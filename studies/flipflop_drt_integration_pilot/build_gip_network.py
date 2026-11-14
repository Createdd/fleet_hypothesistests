"""Build the Klagenfurt simulation network (v2) from the official GIP road graph.

Why a second builder: `build_flipflop_network.py` turned every geometry vertex of
`klagenfurt_network_extended.gpkg` into a node (43k nodes, 15 m edges) and floored every
edge at 30 s, which made vehicles crawl at ~3-4 km/h. The GIP link network
(`data/gip_network_ogd.gpkg`, layer GIP_LINKNETZ_OGD) carries real topology
(FROM_NODE/TO_NODE), modelled car speeds per direction (SPEEDCAR_T/_B), one-way
information and access rights, so travel times come straight from the data.

Output (FleetPy NetworkBasic* format):
  data/networks/klagenfurt_gip/base/{nodes.csv, edges.csv, crs.info}
  data/fleetctrl/initial_vehicle_distribution/klagenfurt_gip/{uniform.csv, moia_origin_density.csv}

Only the largest *strongly* connected component is kept, so every node can reach every
other node and demand preparation needs no separate component filter.
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree

ROOT_DIR = Path(__file__).resolve().parents[2]
GIP_FILE = ROOT_DIR / "data" / "gip_network_ogd.gpkg"
MOIA_FILE = ROOT_DIR / "data" / "demand" / "trips_klagenfurt.csv"
NETWORK_NAME = "klagenfurt_gip"
NETWORK_DIR = ROOT_DIR / "data" / "networks" / NETWORK_NAME / "base"
INIT_DIST_DIR = ROOT_DIR / "data" / "fleetctrl" / "initial_vehicle_distribution" / NETWORK_NAME

# MOIA frame (14.219-14.413, 46.58-46.70) plus margin
BBOX = (14.19, 46.55, 14.45, 46.73)
ACCESS_CAR_BIT = 4  # GIP ACCESS_* bitmask: 1 pedestrian, 2 bike, 4 car, 8 truck, 16 bus, ...
DENSITY_SIGMA_M = 600.0  # kernel width for the demand-weighted vehicle start distribution


def metres_per_degree(lat):
    return 111_320.0, 111_320.0 * np.cos(np.radians(lat))


def main():
    links = gpd.read_file(GIP_FILE, layer="GIP_LINKNETZ_OGD", bbox=BBOX)
    print(f"GIP links in bbox: {len(links):,}")

    # One directed edge per traversable direction. SPEEDCAR_* > 0 is the GIP's own statement
    # that cars may drive that way at that speed (consistent with ONEWAY_CAR, checked).
    car_tow = (links["SPEEDCAR_T"] > 0) & ((links["ACCESS_TOW"] & ACCESS_CAR_BIT) > 0)
    car_bkw = (links["SPEEDCAR_B"] > 0) & ((links["ACCESS_BKW"] & ACCESS_CAR_BIT) > 0)
    print(f"car-traversable: forward {car_tow.sum():,}, backward {car_bkw.sum():,}, "
          f"dropped (no car access either way) {(~(car_tow | car_bkw)).sum():,}")

    # Node coordinates from the link geometry end points (FROM_NODE = first vertex).
    starts = links.geometry.apply(lambda g: list(g.geoms)[0].coords[0])
    ends = links.geometry.apply(lambda g: list(g.geoms)[-1].coords[-1])
    node_pos = {}
    for nid, p in zip(links["FROM_NODE"], starts):
        node_pos.setdefault(int(nid), (p[0], p[1]))
    for nid, p in zip(links["TO_NODE"], ends):
        node_pos.setdefault(int(nid), (p[0], p[1]))

    rows = []
    for direction, mask, speed_col, a, b in (
        ("T", car_tow, "SPEEDCAR_T", "FROM_NODE", "TO_NODE"),
        ("B", car_bkw, "SPEEDCAR_B", "TO_NODE", "FROM_NODE"),
    ):
        sub = links[mask]
        rows.append(pd.DataFrame({
            "gip_from": sub[a].astype(int).values,
            "gip_to": sub[b].astype(int).values,
            "distance": sub["LENGTH"].astype(float).values,
            "travel_time": sub["LENGTH"].astype(float).values / (sub[speed_col].astype(float).values / 3.6),
            "source_edge_id": sub["LINK_ID"].astype(str).values + "_" + direction,
        }))
    edges = pd.concat(rows, ignore_index=True)
    edges = edges[edges["gip_from"] != edges["gip_to"]]
    edges = edges.sort_values("travel_time").drop_duplicates(["gip_from", "gip_to"], keep="first")

    # Largest strongly connected component on the directed graph.
    gip_ids = np.array(sorted(set(edges["gip_from"]) | set(edges["gip_to"])))
    idx = {g: i for i, g in enumerate(gip_ids)}
    fi = edges["gip_from"].map(idx).values
    ti = edges["gip_to"].map(idx).values
    n = len(gip_ids)
    graph = coo_matrix((np.ones(len(edges)), (fi, ti)), shape=(n, n)).tocsr()
    n_comp, labels = connected_components(graph, directed=True, connection="strong")
    largest = np.bincount(labels).argmax()
    keep = labels == largest
    print(f"directed graph: {n:,} nodes, {len(edges):,} edges, {n_comp:,} strong components; "
          f"largest has {keep.sum():,} nodes ({keep.mean():.1%})")

    kept_ids = gip_ids[keep]
    new_idx = {g: i for i, g in enumerate(kept_ids)}
    edges = edges[edges["gip_from"].isin(new_idx) & edges["gip_to"].isin(new_idx)].copy()
    edges["from_node"] = edges["gip_from"].map(new_idx)
    edges["to_node"] = edges["gip_to"].map(new_idx)

    nodes = pd.DataFrame({
        "node_index": np.arange(len(kept_ids)),
        "is_stop_only": 0,
        "pos_x": [node_pos[g][0] for g in kept_ids],
        "pos_y": [node_pos[g][1] for g in kept_ids],
        "gip_node_id": kept_ids,
    })

    NETWORK_DIR.mkdir(parents=True, exist_ok=True)
    nodes.to_csv(NETWORK_DIR / "nodes.csv", index=False)
    edges[["from_node", "to_node", "distance", "travel_time", "source_edge_id"]].to_csv(NETWORK_DIR / "edges.csv", index=False)
    (NETWORK_DIR / "crs.info").write_text("EPSG:4326\n")

    # --- sanity: implied speeds -------------------------------------------------------------
    print(f"edge length m: median {edges['distance'].median():.0f}, mean {edges['distance'].mean():.0f}; "
          f"edge speed km/h (distance-weighted): {edges['distance'].sum() / edges['travel_time'].sum() * 3.6:.1f}")
    n2 = len(kept_ids)
    g2 = coo_matrix((edges["travel_time"].values, (edges["from_node"].values, edges["to_node"].values)), shape=(n2, n2)).tocsr()
    rng = np.random.default_rng(0)
    src = rng.choice(n2, 60, replace=False)
    tt = dijkstra(g2, directed=True, indices=src)
    my, mx = metres_per_degree(nodes["pos_y"].mean())
    xy = np.column_stack([nodes["pos_x"].values * mx, nodes["pos_y"].values * my])
    dst = rng.choice(n2, 60, replace=False)
    bee = np.linalg.norm(xy[src][:, None, :] - xy[dst][None, :, :], axis=2)
    t = tt[:, dst]
    ok = (bee > 2000) & np.isfinite(t)
    print(f"sample OD pairs (>2 km beeline): network time / beeline -> median {np.median(bee[ok] / t[ok] * 3.6):.1f} km/h "
          f"(straight-line equivalent), median network time for 5 km beeline ~ {np.median(t[ok] / bee[ok]) * 5000 / 60:.1f} min")

    # --- vehicle start distributions ----------------------------------------------------------
    INIT_DIST_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"node_index": nodes["node_index"], "probability": 1.0 / n2}).set_index("node_index") \
        .to_csv(INIT_DIST_DIR / "uniform.csv")
    moia = pd.read_csv(MOIA_FILE)
    oxy = np.column_stack([moia["origin_x"].values * mx, moia["origin_y"].values * my])
    tree = cKDTree(oxy)
    # Gaussian kernel density of real MOIA trip origins at every node (+ small floor so no node is impossible)
    neigh = tree.query_ball_point(xy, r=3 * DENSITY_SIGMA_M)
    dens = np.array([
        np.exp(-np.sum((oxy[ids] - xy[i]) ** 2, axis=1) / (2 * DENSITY_SIGMA_M ** 2)).sum() if ids else 0.0
        for i, ids in enumerate(neigh)
    ])
    dens = dens + 0.01 * dens.mean()
    pd.DataFrame({"node_index": nodes["node_index"], "probability": dens / dens.sum()}).set_index("node_index") \
        .to_csv(INIT_DIST_DIR / "moia_origin_density.csv")
    print(f"wrote {NETWORK_DIR} and {INIT_DIST_DIR}")


if __name__ == "__main__":
    main()
