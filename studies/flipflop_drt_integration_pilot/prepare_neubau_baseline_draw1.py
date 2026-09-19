import os

import numpy as np
import pandas as pd


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SAMPLE_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "SampleFiles_recovered",
    "SampleFiles",
    "neubau",
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
    "flipflop_neubau_pilot",
    "matched",
    "flipflop_neubau_extended",
    "draw1_0700_0900_all_modes.csv",
)
MAX_NEAREST_DISTANCE = 0.005
MAX_PILOT_REQUESTS = 100


def nearest_node_ids(points: np.ndarray, nodes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    distances = ((points[:, None, :] - nodes[None, :, :]) ** 2).sum(axis=2)
    nearest_indices = distances.argmin(axis=1)
    nearest_distances = np.sqrt(distances[np.arange(len(points)), nearest_indices])
    return nearest_indices, nearest_distances


def main() -> None:
    samples = pd.read_csv(SAMPLE_FILE, parse_dates=["starting_time"])
    samples = samples[
        (samples["draw"] == 1)
        & (samples["starting_time"].dt.hour.isin([7, 8]))
    ].sort_values(["starting_time", "trip_id"]).copy()
    if samples.empty:
        raise ValueError("No Draw 1 trips found in the 07:00-09:00 window")

    nodes = pd.read_csv(NETWORK_NODES)
    edges = pd.read_csv(NETWORK_EDGES)
    routable_node_ids = pd.unique(edges[["from_node", "to_node"]].to_numpy().ravel())
    nodes = nodes[nodes["node_index"].isin(routable_node_ids)].reset_index(drop=True)
    node_points = nodes[["pos_x", "pos_y"]].to_numpy()
    start_points = samples[["lon_start", "lat_start"]].to_numpy()
    end_points = samples[["lon_end", "lat_end"]].to_numpy()
    start_indices, start_distances = nearest_node_ids(start_points, node_points)
    end_indices, end_distances = nearest_node_ids(end_points, node_points)

    min_lon, max_lon = node_points[:, 0].min(), node_points[:, 0].max()
    min_lat, max_lat = node_points[:, 1].min(), node_points[:, 1].max()
    in_network = (
        (start_points[:, 0] >= min_lon)
        & (start_points[:, 0] <= max_lon)
        & (start_points[:, 1] >= min_lat)
        & (start_points[:, 1] <= max_lat)
        & (end_points[:, 0] >= min_lon)
        & (end_points[:, 0] <= max_lon)
        & (end_points[:, 1] >= min_lat)
        & (end_points[:, 1] <= max_lat)
    )
    in_network &= (start_distances <= MAX_NEAREST_DISTANCE) & (end_distances <= MAX_NEAREST_DISTANCE)

    moia = pd.read_csv(MOIA_FILE)
    moia_x = pd.concat([moia["origin_x"], moia["destination_x"]])
    moia_y = pd.concat([moia["origin_y"], moia["destination_y"]])
    in_moia_frame = (
        samples["lon_start"].between(moia_x.min(), moia_x.max())
        & samples["lat_start"].between(moia_y.min(), moia_y.max())
        & samples["lon_end"].between(moia_x.min(), moia_x.max())
        & samples["lat_end"].between(moia_y.min(), moia_y.max())
    )
    samples = samples[in_moia_frame & in_network].copy()
    samples = samples.head(MAX_PILOT_REQUESTS).copy()

    start_points = samples[["lon_start", "lat_start"]].to_numpy()
    end_points = samples[["lon_end", "lat_end"]].to_numpy()
    start_indices, start_distances = nearest_node_ids(start_points, node_points)
    end_indices, end_distances = nearest_node_ids(end_points, node_points)

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

    print(f"Input rows in Draw 1, 07:00-09:00: {len(in_moia_frame)}")
    print(f"Rows inside common MOIA frame and network coverage: {len(in_moia_frame & in_network)}")
    print(f"Rows retained after network-coverage and identical-node filtering: {len(demand)}")
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