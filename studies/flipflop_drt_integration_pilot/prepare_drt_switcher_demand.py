import argparse
import os

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASELINE_FILE = os.path.join(
    ROOT_DIR, "data", "SampleFiles_recovered", "SampleFiles", "full_draws", "draws_Baseline.csv"
)
MOIA_FILE = os.path.join(ROOT_DIR, "data", "demand", "trips_klagenfurt.csv")
NETWORK_NODES = os.path.join(ROOT_DIR, "data", "networks", "flipflop_neubau_extended", "base", "nodes.csv")
LARGEST_COMPONENT_FILE = os.path.join(
    ROOT_DIR, "data", "fleetctrl", "initial_vehicle_distribution", "flipflop_neubau_extended",
    "largest_component_uniform.csv",
)
MAX_NEAREST_DISTANCE = 0.005
START_HOUR = 6
END_HOUR = 22


def drt_scenario_file(price_scenario: str) -> str:
    return os.path.join(
        ROOT_DIR, "data", "SampleFiles_recovered", "SampleFiles", "full_draws", f"draws_{price_scenario}.csv"
    )


def output_file(price_scenario: str, draw: int) -> str:
    return os.path.join(
        ROOT_DIR,
        "data",
        "demand",
        "flipflop_klagenfurt_switchers_pilot",
        "matched",
        "flipflop_neubau_extended",
        f"switchers_{price_scenario}_draw{draw}_0600_2200.csv",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract realistic FlipFlop DRT mode-switcher demand")
    parser.add_argument("--price-scenario", default="DRT_Kostenx1", help="Suffix of draws_<scenario>.csv to test")
    parser.add_argument("--draw", type=int, default=1, help="FlipFlop draw number (1-5)")
    args = parser.parse_args()

    baseline = pd.read_csv(
        BASELINE_FILE,
        usecols=["draw", "trip_id", "drawn_mode", "starting_time", "lat_start", "lon_start", "lat_end", "lon_end"],
        parse_dates=["starting_time"],
    )
    baseline = baseline[
        (baseline["draw"] == args.draw)
        & (baseline["starting_time"].dt.hour >= START_HOUR)
        & (baseline["starting_time"].dt.hour < END_HOUR)
    ].copy()

    drt = pd.read_csv(drt_scenario_file(args.price_scenario), usecols=["draw", "trip_id", "drawn_mode"])
    drt = drt[drt["draw"] == args.draw]

    moia = pd.read_csv(MOIA_FILE)
    moia_x = pd.concat([moia["origin_x"], moia["destination_x"]])
    moia_y = pd.concat([moia["origin_y"], moia["destination_y"]])
    in_moia_frame = (
        baseline["lon_start"].between(moia_x.min(), moia_x.max())
        & baseline["lat_start"].between(moia_y.min(), moia_y.max())
        & baseline["lon_end"].between(moia_x.min(), moia_x.max())
        & baseline["lat_end"].between(moia_y.min(), moia_y.max())
    )
    baseline = baseline[in_moia_frame].copy()
    print(f"Draw {args.draw}, {START_HOUR:02d}:00-{END_HOUR:02d}:00, MOIA frame: {len(baseline)} trips")

    merged = baseline.merge(drt, on="trip_id", suffixes=("_base", "_drt"))
    switchers = merged[(merged["drawn_mode_base"] != "PT") & (merged["drawn_mode_drt"] == "PT")].copy()
    print(f"Mode-switchers to DRT under {args.price_scenario}: {len(switchers)}")
    if switchers.empty:
        raise ValueError("No switcher trips found for the given draw/price scenario")

    nodes = pd.read_csv(NETWORK_NODES)
    largest_component = pd.read_csv(LARGEST_COMPONENT_FILE)
    connected_node_ids = set(largest_component["node_index"].astype(int))
    nodes = nodes[nodes["node_index"].isin(connected_node_ids)].reset_index(drop=True)
    tree = cKDTree(nodes[["pos_x", "pos_y"]].to_numpy())

    start_points = switchers[["lon_start", "lat_start"]].to_numpy()
    end_points = switchers[["lon_end", "lat_end"]].to_numpy()
    start_distances, start_indices = tree.query(start_points)
    end_distances, end_indices = tree.query(end_points)
    in_network = (start_distances <= MAX_NEAREST_DISTANCE) & (end_distances <= MAX_NEAREST_DISTANCE)
    print(f"Retained after network coverage filter: {int(in_network.sum())}")

    switchers = switchers[in_network].copy()
    switchers["start"] = nodes.iloc[start_indices[in_network]]["node_index"].to_numpy(dtype=int)
    switchers["end"] = nodes.iloc[end_indices[in_network]]["node_index"].to_numpy(dtype=int)

    switchers["rq_time"] = (
        switchers["starting_time"].dt.hour * 3600
        + switchers["starting_time"].dt.minute * 60
        + switchers["starting_time"].dt.second
    )
    switchers = switchers.sort_values(["rq_time", "trip_id"]).reset_index(drop=True)
    switchers["request_id"] = np.arange(len(switchers))

    demand = switchers[["request_id", "rq_time", "start", "end"]].copy()
    demand = demand[demand["start"] != demand["end"]]

    out_path = output_file(args.price_scenario, args.draw)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    demand.to_csv(out_path, index=False)

    print(f"Final demand rows: {len(demand)}")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
