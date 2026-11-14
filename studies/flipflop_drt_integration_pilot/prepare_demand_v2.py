"""Demand preparation v2 for the FlipFlop consistency test (network: klagenfurt_gip).

Differences to the v1 scripts (`prepare_drt_switcher_demand.py`, `prepare_moia_klagenfurt_baseline.py`):
  * all five FlipFlop draws instead of draw 1 only (the per-trip switch decision is a random
    realisation of a ~1.4 pp probability shift; only the spatial-temporal pattern is stable)
  * MOIA demand per real calendar day (7 files) instead of 7 days stacked into one; the stacked
    version is still written for reference
  * full 24 h day instead of 06:00-22:00 (MOIA's real demand peaks 17:00-01:00)
  * snapping onto the GIP network's strongly connected component, max 300 m snap distance

Output: data/demand/flipflop_v2/matched/klagenfurt_gip/<name>.csv  (request_id, rq_time, start, end)
        data/demand/flipflop_v2/demand_summary.csv
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ROOT_DIR = Path(__file__).resolve().parents[2]
DRAWS_DIR = ROOT_DIR / "data" / "SampleFiles_recovered" / "SampleFiles" / "full_draws"
MOIA_FILE = ROOT_DIR / "data" / "demand" / "trips_klagenfurt.csv"
NETWORK_NAME = "klagenfurt_gip"
NODES_FILE = ROOT_DIR / "data" / "networks" / NETWORK_NAME / "base" / "nodes.csv"
OUT_DIR = ROOT_DIR / "data" / "demand" / "flipflop_v2" / "matched" / NETWORK_NAME
SUMMARY_FILE = ROOT_DIR / "data" / "demand" / "flipflop_v2" / "demand_summary.csv"
DRAW_COLS = ["draw", "trip_id", "drawn_mode", "starting_time", "lat_start", "lon_start", "lat_end", "lon_end"]


class Snapper:
    def __init__(self, nodes: pd.DataFrame):
        self.lat0 = nodes["pos_y"].mean()
        self.my, self.mx = 111_320.0, 111_320.0 * np.cos(np.radians(self.lat0))
        self.tree = cKDTree(np.column_stack([nodes["pos_x"] * self.mx, nodes["pos_y"] * self.my]))
        self.node_index = nodes["node_index"].values

    def snap(self, lon, lat):
        d, i = self.tree.query(np.column_stack([np.asarray(lon) * self.mx, np.asarray(lat) * self.my]))
        return self.node_index[i], d


def finalize(df, snapper, max_snap_m, name, summary, extra):
    """Snap origins/destinations, drop unroutable rows, write FleetPy request file."""
    n0 = len(df)
    s, ds = snapper.snap(df["lon_start"], df["lat_start"])
    e, de = snapper.snap(df["lon_end"], df["lat_end"])
    df = df.assign(start=s, end=e, snap_m=np.maximum(ds, de))
    df = df[(df["snap_m"] <= max_snap_m) & (df["start"] != df["end"])]
    df = df.sort_values("rq_time").reset_index(drop=True)
    out = pd.DataFrame({"request_id": np.arange(len(df)), "rq_time": df["rq_time"].astype(int),
                        "start": df["start"].astype(int), "end": df["end"].astype(int)})
    out.to_csv(OUT_DIR / f"{name}.csv", index=False)
    summary.append({"name": name, **extra, "rows_in": n0, "rows_out": len(out),
                    "snap_p90_m": round(float(df["snap_m"].quantile(0.9)), 1) if len(df) else None})
    print(f"  {name:45s} {n0:7,d} -> {len(out):6,d}")


def moia_frame(moia):
    x = pd.concat([moia["origin_x"], moia["destination_x"]])
    y = pd.concat([moia["origin_y"], moia["destination_y"]])
    return x.min(), x.max(), y.min(), y.max()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--price-scenarios", nargs="+", default=["DRT_Kostenx1"], help="draws_<name>.csv to compare with draws_Baseline.csv")
    ap.add_argument("--draws", nargs="+", type=int, default=[1, 2, 3, 4, 5])
    ap.add_argument("--max-snap-m", type=float, default=300.0)
    ap.add_argument("--skip-flipflop", action="store_true")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    snapper = Snapper(pd.read_csv(NODES_FILE))
    moia = pd.read_csv(MOIA_FILE)
    x0, x1, y0, y1 = moia_frame(moia)
    summary = []

    # --- real MOIA trips: per calendar day and stacked ----------------------------------------
    print("MOIA")
    day = moia["departure_time"] // 86400
    day = day - day.min()
    base = pd.DataFrame({"rq_time": moia["departure_time"] % 86400, "lon_start": moia["origin_x"], "lat_start": moia["origin_y"],
                         "lon_end": moia["destination_x"], "lat_end": moia["destination_y"], "day": day})
    for d in sorted(base["day"].unique()):
        finalize(base[base["day"] == d], snapper, args.max_snap_m, f"moia_day{d}", summary, {"source": "moia", "day": int(d)})
    finalize(base, snapper, args.max_snap_m, "moia_pooled7", summary, {"source": "moia", "day": "pooled"})

    # --- FlipFlop mode switchers, per draw and price scenario --------------------------------
    if not args.skip_flipflop:
        print("FlipFlop (loading baseline draws ...)")
        baseline = pd.read_csv(DRAWS_DIR / "draws_Baseline.csv", usecols=DRAW_COLS, parse_dates=["starting_time"])
        in_frame = (baseline["lon_start"].between(x0, x1) & baseline["lat_start"].between(y0, y1)
                    & baseline["lon_end"].between(x0, x1) & baseline["lat_end"].between(y0, y1))
        baseline = baseline[in_frame & baseline["draw"].isin(args.draws)].copy()
        baseline["rq_time"] = (baseline["starting_time"].dt.hour * 3600 + baseline["starting_time"].dt.minute * 60
                               + baseline["starting_time"].dt.second)
        for scen in args.price_scenarios:
            drt = pd.read_csv(DRAWS_DIR / f"draws_{scen}.csv", usecols=["draw", "trip_id", "drawn_mode"])
            drt = drt[drt["draw"].isin(args.draws)]
            merged = baseline.merge(drt, on=["draw", "trip_id"], suffixes=("_base", "_drt"))
            switch = merged[(merged["drawn_mode_base"] != "PT") & (merged["drawn_mode_drt"] == "PT")]
            for d in args.draws:
                finalize(switch[switch["draw"] == d], snapper, args.max_snap_m, f"switchers_{scen}_draw{d}", summary,
                         {"source": "flipflop", "scenario": scen, "draw": d})

    pd.DataFrame(summary).to_csv(SUMMARY_FILE, index=False)
    print(f"summary -> {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
