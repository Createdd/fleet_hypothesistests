"""Convert raw Klagenfurt trip coordinates into FleetPy request format.

Input:
- data/demand/trips_klagenfurt.csv
  columns: departure_time, origin_x, origin_y, destination_x, destination_y

Output:
- data/demand/klagenfurt_h1_spitzenzeiten/matched/klagenfurt_h1_spitzenzeiten/demand_requests_trips.csv
  columns: Unnamed: 0, request_id, rq_time, start, end, earliest_pickup_time

Notes:
- departure_time is mapped to seconds-of-day via modulo 86400 by default.
- Origin and destination coordinates are snapped to nearest network node.
- Optional filters allow keeping only requests with endpoints in network bbox.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_INPUT = Path("data/demand/trips_klagenfurt.csv")
DEFAULT_NODES = Path("data/networks/klagenfurt_h1_spitzenzeiten/base/nodes.csv")
DEFAULT_OUTPUT = Path(
    "data/demand/klagenfurt_h1_spitzenzeiten/matched/klagenfurt_h1_spitzenzeiten/demand_requests_trips.csv"
)


def nearest_node_ids(x: np.ndarray, y: np.ndarray, nodes_xy: np.ndarray, node_ids: np.ndarray) -> np.ndarray:
    # Brute-force nearest-neighbor is acceptable for current scale (~1k trips, ~3.4k nodes).
    points = np.column_stack([x, y])
    d2 = ((points[:, None, :] - nodes_xy[None, :, :]) ** 2).sum(axis=2)
    return node_ids[np.argmin(d2, axis=1)]


def build_requests(
    trips_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
    start_time: int,
    end_time: int,
    use_seconds_of_day: bool,
    require_bbox: bool,
) -> pd.DataFrame:
    required_cols = {"departure_time", "origin_x", "origin_y", "destination_x", "destination_y"}
    missing = required_cols.difference(trips_df.columns)
    if missing:
        raise ValueError(f"Missing required columns in trips file: {sorted(missing)}")

    min_x, max_x = nodes_df["pos_x"].min(), nodes_df["pos_x"].max()
    min_y, max_y = nodes_df["pos_y"].min(), nodes_df["pos_y"].max()

    if require_bbox:
        o_in = trips_df["origin_x"].between(min_x, max_x) & trips_df["origin_y"].between(min_y, max_y)
        d_in = trips_df["destination_x"].between(min_x, max_x) & trips_df["destination_y"].between(min_y, max_y)
        trips_df = trips_df[o_in & d_in].copy()

    rq_time = trips_df["departure_time"].to_numpy(dtype=np.int64)
    if use_seconds_of_day:
        rq_time = rq_time % 86400

    time_mask = (rq_time >= start_time) & (rq_time < end_time)
    trips_df = trips_df.loc[time_mask].copy()
    rq_time = rq_time[time_mask]

    nodes_xy = nodes_df[["pos_x", "pos_y"]].to_numpy(dtype=np.float64)
    node_ids = nodes_df["node_index"].to_numpy(dtype=np.int64)

    starts = nearest_node_ids(
        trips_df["origin_x"].to_numpy(dtype=np.float64),
        trips_df["origin_y"].to_numpy(dtype=np.float64),
        nodes_xy,
        node_ids,
    )
    ends = nearest_node_ids(
        trips_df["destination_x"].to_numpy(dtype=np.float64),
        trips_df["destination_y"].to_numpy(dtype=np.float64),
        nodes_xy,
        node_ids,
    )

    out = pd.DataFrame(
        {
            "Unnamed: 0": np.arange(len(trips_df), dtype=np.float64),
            "request_id": np.arange(len(trips_df), dtype=np.float64),
            "rq_time": rq_time.astype(np.float64),
            "start": starts.astype(np.float64),
            "end": ends.astype(np.float64),
            "earliest_pickup_time": rq_time.astype(np.float64),
        }
    )

    out = out[out["start"] != out["end"]].copy()
    out.sort_values("rq_time", inplace=True)
    out.reset_index(drop=True, inplace=True)
    out["Unnamed: 0"] = np.arange(len(out), dtype=np.float64)
    out["request_id"] = np.arange(len(out), dtype=np.float64)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert trips_klagenfurt.csv to FleetPy demand requests")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to trips CSV")
    parser.add_argument("--nodes", default=str(DEFAULT_NODES), help="Path to network nodes.csv")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output request CSV path")
    parser.add_argument("--start-time", type=int, default=21600, help="Inclusive time filter [s]")
    parser.add_argument("--end-time", type=int, default=79200, help="Exclusive time filter [s]")
    parser.add_argument(
        "--no-seconds-of-day",
        action="store_true",
        help="Use departure_time as-is (do not apply modulo 86400)",
    )
    parser.add_argument(
        "--require-bbox",
        action="store_true",
        help="Keep only trips whose origin and destination are inside network bbox",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    nodes_path = Path(args.nodes)
    output_path = Path(args.output)

    trips_df = pd.read_csv(input_path)
    nodes_df = pd.read_csv(nodes_path)

    result = build_requests(
        trips_df=trips_df,
        nodes_df=nodes_df,
        start_time=args.start_time,
        end_time=args.end_time,
        use_seconds_of_day=not args.no_seconds_of_day,
        require_bbox=args.require_bbox,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    print(f"Input rows: {len(trips_df)}")
    print(f"Output rows: {len(result)}")
    print(f"Output file: {output_path}")
    if len(result) > 0:
        print(f"rq_time range: {int(result['rq_time'].min())} - {int(result['rq_time'].max())}")


if __name__ == "__main__":
    main()
