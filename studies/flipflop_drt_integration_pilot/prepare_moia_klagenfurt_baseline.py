import os

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOIA_FILE = os.path.join(ROOT_DIR, "data", "demand", "trips_klagenfurt.csv")
NETWORK_NODES = os.path.join(
    ROOT_DIR, "data", "networks", "flipflop_neubau_extended", "base", "nodes.csv"
)
LARGEST_COMPONENT_FILE = os.path.join(
    ROOT_DIR, "data", "fleetctrl", "initial_vehicle_distribution", "flipflop_neubau_extended",
    "largest_component_uniform.csv",
)
OUTPUT_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "demand",
    "moia_klagenfurt_pilot",
    "matched",
    "flipflop_neubau_extended",
    "moia_baseline_0600_2200.csv",
)
MAX_NEAREST_DISTANCE = 0.005
# Full operating day (06:00-22:00), matching the H-A switcher-demand convention.
# The raw log spans 7 real days (departure_time // 86400 in {0..6}); folding all
# of them into one simulated day via "% 86400" is the same convention this
# repo's convert_trips_klagenfurt_to_requests.py already uses elsewhere. It means
# this demand file represents roughly 7 real days of MOIA trips compressed into
# a single simulated day, not one real day's volume - see the model-validity
# notebook for the per-day-average framing of this.
START_TIME = 21600
END_TIME = 79200


def main() -> None:
    trips = pd.read_csv(MOIA_FILE)
    seconds_of_day = trips["departure_time"] % 86400
    trips = trips[(seconds_of_day >= START_TIME) & (seconds_of_day < END_TIME)].copy()
    trips["rq_time"] = seconds_of_day.loc[trips.index]
    trips = trips.sort_values("rq_time").reset_index(drop=True)
    if trips.empty:
        raise ValueError("No MOIA trips found in the 06:00-22:00 window")

    nodes = pd.read_csv(NETWORK_NODES)
    largest_component = pd.read_csv(LARGEST_COMPONENT_FILE)
    connected_node_ids = set(largest_component["node_index"].astype(int))
    nodes = nodes[nodes["node_index"].isin(connected_node_ids)].reset_index(drop=True)
    tree = cKDTree(nodes[["pos_x", "pos_y"]].to_numpy())

    start_points = trips[["origin_x", "origin_y"]].to_numpy()
    end_points = trips[["destination_x", "destination_y"]].to_numpy()
    start_distances, start_indices = tree.query(start_points)
    end_distances, end_indices = tree.query(end_points)
    in_network = (start_distances <= MAX_NEAREST_DISTANCE) & (end_distances <= MAX_NEAREST_DISTANCE)
    print(f"MOIA rows in 06:00-22:00 window (pooled across ~7 real days): {len(trips)}")
    print(f"Rows inside network coverage: {int(in_network.sum())}")

    trips = trips[in_network].copy()
    start_indices = start_indices[in_network]
    end_indices = end_indices[in_network]

    trips["request_id"] = np.arange(len(trips))
    trips["start"] = nodes.iloc[start_indices]["node_index"].to_numpy(dtype=int)
    trips["end"] = nodes.iloc[end_indices]["node_index"].to_numpy(dtype=int)
    demand = trips[["request_id", "rq_time", "start", "end"]].copy()
    demand = demand[demand["start"] != demand["end"]]

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    demand.to_csv(OUTPUT_FILE, index=False)

    print(f"Rows retained after identical-node filtering: {len(demand)}")
    print(f"Wrote: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
