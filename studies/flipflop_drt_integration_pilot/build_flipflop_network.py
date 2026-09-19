from pathlib import Path

import geopandas as gpd
import networkx as nx
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
SOURCE_FILE = ROOT_DIR / "klagenfurt_network_extended.gpkg"
NETWORK_DIR = ROOT_DIR / "data" / "networks" / "flipflop_neubau_extended" / "base"
INIT_DIST_DIR = ROOT_DIR / "data" / "fleetctrl" / "initial_vehicle_distribution" / "flipflop_neubau_extended"


def main() -> None:
    source = gpd.read_file(SOURCE_FILE)
    node_keys = {}
    node_rows = []
    edge_rows = []

    def get_node_id(x: float, y: float) -> int:
        key = (round(float(x), 7), round(float(y), 7))
        if key not in node_keys:
            node_keys[key] = len(node_rows)
            node_rows.append({
                "node_index": node_keys[key],
                "is_stop_only": 0,
                "pos_x": key[0],
                "pos_y": key[1],
            })
        return node_keys[key]

    for geometry in source.geometry:
        lines = geometry.geoms if hasattr(geometry, "geoms") else [geometry]
        for line in lines:
            coordinates = list(line.coords)
            for start, end in zip(coordinates[:-1], coordinates[1:]):
                start_id = get_node_id(*start[:2])
                end_id = get_node_id(*end[:2])
                if start_id == end_id:
                    continue
                distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5 * 111000
                travel_time = max(30.0, distance / (50_000 / 3600))
                edge_rows.extend([
                    {"from_node": start_id, "to_node": end_id, "distance": distance, "travel_time": travel_time, "source_edge_id": None},
                    {"from_node": end_id, "to_node": start_id, "distance": distance, "travel_time": travel_time, "source_edge_id": None},
                ])

    nodes = pd.DataFrame(node_rows)
    edges = pd.DataFrame(edge_rows)
    NETWORK_DIR.mkdir(parents=True, exist_ok=True)
    nodes.to_csv(NETWORK_DIR / "nodes.csv", index=False)
    edges.to_csv(NETWORK_DIR / "edges.csv", index=False)
    (NETWORK_DIR / "crs.info").write_text("EPSG:4326\n")
    graph = nx.Graph()
    graph.add_edges_from(edges[["from_node", "to_node"]].itertuples(index=False, name=None))
    largest_component = max(nx.connected_components(graph), key=len)
    init_distribution = pd.DataFrame({
        "node_index": sorted(largest_component),
        "probability": 1.0 / len(largest_component),
    }).set_index("node_index")
    INIT_DIST_DIR.mkdir(parents=True, exist_ok=True)
    init_distribution.to_csv(INIT_DIST_DIR / "largest_component_uniform.csv")
    print(f"Wrote {len(nodes):,} nodes and {len(edges):,} bidirectional edges")
    print(f"Largest connected component: {len(largest_component):,} nodes")
    print(f"Network directory: {NETWORK_DIR}")


if __name__ == "__main__":
    main()