"""Run v2 consistency-test scenarios (file-based entry point so multiprocessing works on macOS).

macOS uses the 'spawn' start method: worker processes re-import __main__, which fails when the
driver is `python -` / a notebook cell and silently loops forever. Always launch sweeps through
this file.

Usage (from repo root):
  python studies/flipflop_drt_integration_pilot/run_v2.py scenario_cfg_v2_probe.csv --parallel 2
  python studies/flipflop_drt_integration_pilot/run_v2.py scenario_cfg_v2_sweep.csv --parallel 6 --skip-done
"""
import argparse
import os
import sys
import time
from datetime import timedelta

import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)
STUDY_DIR = os.path.join(ROOT_DIR, "studies", "flipflop_drt_integration_pilot")
SCENARIO_DIR = os.path.join(STUDY_DIR, "scenarios")
RESULTS_DIR = os.path.join(STUDY_DIR, "results")


def main():
    from run_examples import run_scenarios  # noqa: E402  (after sys.path)

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenario_csv", help="file name in scenarios/ (or a path)")
    ap.add_argument("--const-cfg", default="const_cfg_v2_consistency.yaml")
    ap.add_argument("--parallel", type=int, default=1, help="simulations run side by side")
    ap.add_argument("--skip-done", action="store_true", help="skip scenarios whose standard_eval.csv already exists")
    ap.add_argument("--only", nargs="*", help="run only these scenario names")
    ap.add_argument("--log-level", default="warning")
    args = ap.parse_args()

    scen_path = args.scenario_csv if os.path.exists(args.scenario_csv) else os.path.join(SCENARIO_DIR, args.scenario_csv)
    const_path = args.const_cfg if os.path.exists(args.const_cfg) else os.path.join(SCENARIO_DIR, args.const_cfg)
    df = pd.read_csv(scen_path)
    if args.only:
        df = df[df["scenario_name"].isin(args.only)]
    if args.skip_done:
        done = df["scenario_name"].apply(lambda s: os.path.exists(os.path.join(RESULTS_DIR, s, "standard_eval.csv")))
        print(f"skipping {int(done.sum())} finished scenarios")
        df = df[~done]
    if df.empty:
        print("nothing to run")
        return
    tmp = os.path.join(SCENARIO_DIR, f"_run_{os.path.basename(scen_path)}")
    df.to_csv(tmp, index=False)
    print(f"{len(df)} scenarios, {args.parallel} in parallel, start {time.strftime('%H:%M:%S')}", flush=True)
    t0 = time.time()
    try:
        run_scenarios(const_path, tmp, log_level=args.log_level, n_cpu_per_sim=1, n_parallel_sim=args.parallel,
                      continue_next_after_error=True)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    print(f"finished {time.strftime('%H:%M:%S')}, wall time {timedelta(seconds=int(time.time() - t0))}", flush=True)
    for s in df["scenario_name"]:
        ok = os.path.exists(os.path.join(RESULTS_DIR, s, "standard_eval.csv"))
        print(f"  {'OK ' if ok else 'MISSING'} {s}")


if __name__ == "__main__":
    main()
