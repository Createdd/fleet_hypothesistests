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


def gurobi_problem(const_path, scenarios=None):
    """FleetPy's Alonso-Mora assignment needs Gurobi. If Gurobi cannot start (e.g. expired license),
    FleetPy retries for up to 300 s per optimisation step and then silently continues WITHOUT
    optimising, so a sweep would run for days and produce wrong results. Returns an error text or None."""
    try:
        import yaml
        with open(const_path) as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:  # noqa: BLE001  (non-yaml configs: nothing to check here)
        return None
    if cfg.get("op_rp_batch_optimizer") != "AlonsoMora":
        return None
    default = str(cfg.get("op_solver", "Gurobi"))
    if scenarios is not None and "op_solver" in scenarios:
        solvers = set(scenarios["op_solver"].fillna(default).astype(str))
    else:
        solvers = {default}
    if "Gurobi" not in solvers:
        return None
    try:
        import gurobipy
        with gurobipy.Env(empty=True) as env:
            env.setParam("OutputFlag", 0)
            env.start()
    except Exception as e:  # noqa: BLE001  (any failure to start Gurobi blocks the sweep)
        return f"Gurobi cannot start: {e}"
    return None


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
        unknown = sorted(set(args.only) - set(df["scenario_name"]))
        if unknown:
            print(f"unknown scenario name(s) for --only: {', '.join(unknown)}", file=sys.stderr)
            return 2
        df = df[df["scenario_name"].isin(args.only)]
    if args.skip_done:
        done = df["scenario_name"].apply(lambda s: os.path.exists(os.path.join(RESULTS_DIR, s, "standard_eval.csv")))
        print(f"skipping {int(done.sum())} finished scenarios")
        df = df[~done]
    if df.empty:
        print("nothing to run")
        return 0
    problem = gurobi_problem(const_path, df)
    if problem:
        print(f"{problem}\nNo scenario started. Renew the Gurobi license (e.g. grbgetkey) and run again.", file=sys.stderr)
        return 3
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
    failed = []
    for s in df["scenario_name"]:
        # a result only counts if it was (re)written by this run; an older standard_eval.csv must not hide a failure
        f = os.path.join(RESULTS_DIR, s, "standard_eval.csv")
        ok = os.path.exists(f) and os.path.getmtime(f) >= t0
        print(f"  {'OK ' if ok else 'MISSING'} {s}")
        if not ok:
            failed.append(s)
    if failed:
        print(f"{len(failed)} of {len(df)} scenarios failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
