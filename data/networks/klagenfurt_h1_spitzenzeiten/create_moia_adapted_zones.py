#!/usr/bin/env python3
"""
Create MOIA-adapted zone system for Klagenfurt.

This script:
1) Loads MOIA trips (origins + destinations).
2) Removes extreme outliers by quantile bounds.
3) Builds KMeans zones on MOIA points.
4) Assigns network nodes to nearest zone centroid.
5) Generates centroid nodes per zone.
6) Writes node_zone_info.csv and moia_zone_polygons.geojson.
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import geopandas as gpd
from shapely.geometry import Point, MultiPoint


def find_repo_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / "studies").is_dir() and (parent / "run_uc2_age_based.py").exists():
            return parent
    return start

ROOT = find_repo_root(Path(__file__).resolve())
TRIPS_FILE = ROOT / "data" / "demand" / "trips_klagenfurt.csv"
NODES_FILE = ROOT / "data" / "networks" / "klagenfurt_h1_spitzenzeiten" / "base" / "backup_fullnetwork" / "nodes.csv"
OUT_DIR = ROOT / "data" / "zones" / "klagenfurt_h1_spitzenzeiten" / "adapted_to_moia_data"


def load_points(trips_path: Path) -> np.ndarray:
    trips = pd.read_csv(trips_path)
    origins = trips[["origin_x", "origin_y"]].rename(columns={"origin_x": "x", "origin_y": "y"})
    dests = trips[["destination_x", "destination_y"]].rename(columns={"destination_x": "x", "destination_y": "y"})
    points = pd.concat([origins, dests], ignore_index=True)
    return points


def filter_outliers(points: pd.DataFrame, q_low: float, q_high: float) -> pd.DataFrame:
    x_low, x_high = points["x"].quantile([q_low, q_high])
    y_low, y_high = points["y"].quantile([q_low, q_high])
    mask = points["x"].between(x_low, x_high) & points["y"].between(y_low, y_high)
    return points[mask].copy()


def select_centroids(coords: np.ndarray, n_centroids: int) -> np.ndarray:
    if len(coords) == 0:
        return np.array([], dtype=int)
    n_centroids = min(n_centroids, len(coords))
    mean_coord = coords.mean(axis=0, keepdims=True)
    first_idx = cdist(coords, mean_coord).argmin()
    selected = [first_idx]
    for _ in range(n_centroids - 1):
        selected_coords = coords[selected]
        min_distances = cdist(coords, selected_coords).min(axis=1)
        next_idx = min_distances.argmax()
        selected.append(next_idx)
    return np.array(selected, dtype=int)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create MOIA-adapted zones")
    parser.add_argument("--n-zones", type=int, default=8, help="Number of zones")
    parser.add_argument("--q-low", type=float, default=0.001, help="Lower quantile for outlier filter")
    parser.add_argument("--q-high", type=float, default=0.999, help="Upper quantile for outlier filter")
    parser.add_argument("--centroids-per-zone", type=int, default=50, help="Centroids per zone")
    args = parser.parse_args()

    points = load_points(TRIPS_FILE)
    filtered = filter_outliers(points, args.q_low, args.q_high)

    if filtered.empty:
        raise ValueError("Outlier filtering removed all points; adjust quantiles.")

    kmeans = KMeans(n_clusters=args.n_zones, random_state=0, n_init="auto")
    kmeans.fit(filtered[["x", "y"]].to_numpy(dtype=float))
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # Build zone polygons from MOIA points
    gdf_points = gpd.GeoDataFrame(
        filtered.copy(),
        geometry=gpd.points_from_xy(filtered["x"], filtered["y"]),
        crs="EPSG:4326",
    )
    gdf_points["zone_id"] = labels

    polys = []
    for zone_id, group in gdf_points.groupby("zone_id"):
        hull = MultiPoint(list(group.geometry)).convex_hull
        polys.append({"zone_id": int(zone_id), "geometry": hull})

    poly_gdf = gpd.GeoDataFrame(polys, geometry="geometry", crs="EPSG:4326")

    # Assign network nodes to nearest centroid
    nodes = pd.read_csv(NODES_FILE)
    node_coords = nodes[["pos_x", "pos_y"]].to_numpy(dtype=float)
    dist = cdist(node_coords, centers)
    node_zone = dist.argmin(axis=1)

    zone_info = pd.DataFrame({
        "node_index": nodes["node_index"],
        "zone_id": node_zone.astype(int),
        "is_centroid": 0,
        "is_boarding_node": 1,
    })

    # Select centroids per zone from nodes
    all_centroids = []
    for zone_id in range(args.n_zones):
        zone_nodes = nodes[node_zone == zone_id]
        if zone_nodes.empty:
            continue
        coords = zone_nodes[["pos_x", "pos_y"]].to_numpy(dtype=float)
        selected_idx = select_centroids(coords, args.centroids_per_zone)
        centroids = zone_nodes.iloc[selected_idx]["node_index"].tolist()
        all_centroids.extend(centroids)

    zone_info.loc[zone_info["node_index"].isin(all_centroids), "is_centroid"] = 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    zone_info.to_csv(OUT_DIR / "node_zone_info.csv", index=False)
    poly_gdf.to_file(OUT_DIR / "moia_zone_polygons.geojson", driver="GeoJSON")

    print("MOIA-adapted zones written to:")
    print(f"- {OUT_DIR / 'node_zone_info.csv'}")
    print(f"- {OUT_DIR / 'moia_zone_polygons.geojson'}")


if __name__ == "__main__":
    main()
