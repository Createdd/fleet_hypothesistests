"""Evaluate v2 consistency-test runs (results/v2_*).

For every scenario the script reads FleetPy's standard_eval.csv (fleet-level KPIs) and
1_user-stats.csv (per-request pickup/dropoff times) and derives the level of service that
the simulated fleet actually delivered, so it can be held against the level of service the
FlipFlop choice model *assumed* when it predicted the demand:

  * AIT README: "DRT reduziert Zugangszeit auf 30 %" of the PT access time (Ø 21 min)
    -> assumed door-to-door access ~ 6.3 min. Operationalised here as request-to-pickup wait.
  * AIT README: "DRT Fahrzeit = 50/50 Mix aus Auto- und PT-Fahrzeit". Without PT times we
    only report the in-vehicle detour relative to the direct car route.

Both thresholds are explicit assumptions until AIT provides the absolute per-trip values.

Usage: python studies/flipflop_drt_integration_pilot/evaluate_v2.py [--wait-threshold-min 6.3] [--pattern 'v2_*']
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT_DIR / "studies" / "flipflop_drt_integration_pilot" / "results"
# v2_<source>_<set>_f<fleet>  or  v2w6_... for runs whose op_max_wait_time was set to the assumed 6.3 min
NAME_RE = re.compile(r"^v2(?P<variant>w\d+)?_(?:probe_)?(?P<source>moia|ff|switchers)_(?P<set>[a-z0-9]+)_f(?P<fleet>\d+)$")


def evaluate_scenario(path: Path, wait_threshold_s: float, detour_threshold: float) -> dict:
    ev = pd.read_csv(path / "standard_eval.csv", index_col=0).iloc[:, 0]
    us = pd.read_csv(path / "1_user-stats.csv")
    served = us[us["operator_id"].notna()].copy()
    served["wait_s"] = served["pickup_time"] - served["rq_time"]
    served["ivt_s"] = served["dropoff_time"] - served["pickup_time"]
    served["detour"] = served["ivt_s"] / served["direct_route_travel_time"].replace(0, np.nan)
    n = len(us)
    within = served[(served["wait_s"] <= wait_threshold_s) & (served["detour"] <= detour_threshold)]
    m = NAME_RE.match(path.name)
    return {
        "scenario": path.name,
        "variant": (m["variant"] or "") if m else "",
        "source": m["source"] if m else None,
        "set": m["set"] if m else None,
        "fleet": int(m["fleet"]) if m else None,
        "requests": n,
        "served_pct": 100 * len(served) / n if n else np.nan,
        "served_within_assumed_los_pct": 100 * len(within) / n if n else np.nan,
        "wait_median_min": served["wait_s"].median() / 60,
        "wait_p90_min": served["wait_s"].quantile(0.9) / 60,
        "detour_median": served["detour"].median(),
        "direct_tt_median_min": us["direct_route_travel_time"].median() / 60,
        "rides_per_veh_h": float(ev.get("rides per veh rev hours", np.nan)),
        "occupancy": float(ev.get("occupancy", np.nan)),
        "fleet_util_pct": float(ev.get("% fleet utilization", np.nan)),
        "empty_vkm_pct": float(ev.get("% empty vkm", np.nan)),
        "avg_drive_kmh": float(ev.get("avg driving velocity [km/h]", np.nan)),
        "total_vkm": float(ev.get("total vkm", np.nan)),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wait-threshold-min", type=float, default=6.3, help="assumed DRT access time (0.3 x 21 min PT access)")
    ap.add_argument("--detour-threshold", type=float, default=1.4, help="max in-vehicle time / direct car time")
    ap.add_argument("--pattern", default="v2_*")
    ap.add_argument("--out", default=str(RESULTS_DIR / "v2_evaluation.csv"))
    args = ap.parse_args()

    rows = []
    for d in sorted(RESULTS_DIR.glob(args.pattern)):
        if (d / "standard_eval.csv").exists() and (d / "1_user-stats.csv").exists():
            rows.append(evaluate_scenario(d, args.wait_threshold_min * 60, args.detour_threshold))
    if not rows:
        print("no completed v2 scenarios found")
        return
    df = pd.DataFrame(rows).sort_values(["source", "fleet", "set"])
    df.to_csv(args.out, index=False)
    pd.set_option("display.width", 220)
    print(df[["scenario", "requests", "served_pct", "served_within_assumed_los_pct", "wait_median_min", "wait_p90_min",
              "detour_median", "rides_per_veh_h", "occupancy", "fleet_util_pct"]].round(2).to_string(index=False))

    # fleet-level aggregate across days (MOIA) / draws (FlipFlop)
    agg = df.groupby(["source", "fleet"]).agg(
        runs=("scenario", "size"), requests_mean=("requests", "mean"),
        served_mean=("served_pct", "mean"), served_min=("served_pct", "min"), served_max=("served_pct", "max"),
        within_los_mean=("served_within_assumed_los_pct", "mean"),
        wait_median_mean=("wait_median_min", "mean"), rides_per_veh_h=("rides_per_veh_h", "mean"),
    ).round(1)
    print("\nper fleet size (mean over days / draws):")
    print(agg.to_string())
    print(f"\nassumed LOS: wait <= {args.wait_threshold_min} min and in-vehicle time <= {args.detour_threshold} x direct")
    print(f"written: {args.out}")


if __name__ == "__main__":
    main()
