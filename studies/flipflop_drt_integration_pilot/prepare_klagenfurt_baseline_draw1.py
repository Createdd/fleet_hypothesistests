import os

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SAMPLE_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "SampleFiles_recovered",
    "SampleFiles",
    "full_draws",
    "draws_Baseline.csv",
)
MOIA_FILE = os.path.join(ROOT_DIR, "data", "demand", "trips_klagenfurt.csv")
NETWORK_NODES = os.path.join(
    ROOT_DIR, "data", "networks", "flipflop_neubau_extended", "base", "nodes.csv"
)
NETWORK_EDGES = os.path.join(
    ROOT_DIR, "data", "networks", "flipflop_neubau_extended", "base", "edges.csv"
)
OUTPUT_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "demand",
    "flipflop_klagenfurt_pilot",
    "matched",
    "flipflop_neubau_extended",
    "draw1_0700_0900_all_modes.csv",
)
MAX_NEAREST_DISTANCE = 0.005
MAX_PILOT_REQUESTS = 100
DRAW = 1


def nearest_node_ids(points: np.ndarray, tree: cKDTree) -> tuple[np.ndarray, np.ndarray]:
    nearest_distances, nearest_indices = tree.query(points)
    return nearest_indices, nearest_distances


def main() -> None:
    samples = pd.read_csv(SAMPLE_FILE, parse_dates=["starting_time"])
    samples = samples[
        (samples["draw"] == DRAW)
        & (samples["starting_time"].dt.hour.isin([7, 8]))
    ].sort_values(["starting_time", "trip_id"]).copy()
    if samples.empty:
        raise ValueError(f"No Draw {DRAW} trips found in the 07:00-09:00 window")

    nodes = pd.read_csv(NETWORK_NODES)
    edges = pd.read_csv(NETWORK_EDGES)
    routable_node_ids = pd.unique(edges[["from_node", "to_node"]].to_numpy().ravel())
    nodes = nodes[nodes["node_index"].isin(routable_node_ids)].reset_index(drop=True)
    node_points = nodes[["pos_x", "pos_y"]].to_numpy()
    tree = cKDTree(node_points)

    moia = pd.read_csv(MOIA_FILE)
    moia_x = pd.concat([moia["origin_x"], moia["destination_x"]])
    moia_y = pd.concat([moia["origin_y"], moia["destination_y"]])
    in_moia_frame = (
        samples["lon_start"].between(moia_x.min(), moia_x.max())
        & samples["lat_start"].between(moia_y.min(), moia_y.max())
        & samples["lon_end"].between(moia_x.min(), moia_x.max())
        & samples["lat_end"].between(moia_y.min(), moia_y.max())
    )
    print(f"Draw {DRAW} rows in 07:00-09:00 window: {len(samples)}")
    print(f"Rows inside common MOIA frame: {int(in_moia_frame.sum())}")
    samples = samples[in_moia_frame].copy()

    start_points = samples[["lon_start", "lat_start"]].to_numpy()
    end_points = samples[["lon_end", "lat_end"]].to_numpy()
    start_indices, start_distances = nearest_node_ids(start_points, tree)
    end_indices, end_distances = nearest_node_ids(end_points, tree)
    in_network = (start_distances <= MAX_NEAREST_DISTANCE) & (end_distances <= MAX_NEAREST_DISTANCE)
    print(f"Rows inside MOIA frame and network coverage: {int(in_network.sum())}")

    samples = samples[in_network].copy()
    samples = samples.head(MAX_PILOT_REQUESTS).copy()

    start_points = samples[["lon_start", "lat_start"]].to_numpy()
    end_points = samples[["lon_end", "lat_end"]].to_numpy()
    start_indices, start_distances = nearest_node_ids(start_points, tree)
    end_indices, end_distances = nearest_node_ids(end_points, tree)

    samples["request_id"] = samples["trip_id"].astype(int)
    samples["rq_time"] = (
        samples["starting_time"].dt.hour * 3600
        + samples["starting_time"].dt.minute * 60
        + samples["starting_time"].dt.second
    )
    samples["start"] = nodes.iloc[start_indices]["node_index"].to_numpy(dtype=int)
    samples["end"] = nodes.iloc[end_indices]["node_index"].to_numpy(dtype=int)
    demand = samples[["request_id", "rq_time", "start", "end"]].copy()
    demand = demand[demand["start"] != demand["end"]]

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    demand.to_csv(OUTPUT_FILE, index=False)

    print(f"Rows retained after identical-node filtering and pilot cap ({MAX_PILOT_REQUESTS}): {len(demand)}")
    print(f"Mode distribution of retained rows:\n{samples['drawn_mode'].value_counts().to_string()}")
    print(
        "Nearest start distance, coordinate units: "
        f"min={start_distances.min():.6f}, "
        f"median={np.median(start_distances):.6f}, "
        f"max={start_distances.max():.6f}"
    )
    print(
        "Nearest end distance, coordinate units: "
        f"min={end_distances.min():.6f}, "
        f"median={np.median(end_distances):.6f}, "
        f"max={end_distances.max():.6f}"
    )
    print(f"Wrote: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
