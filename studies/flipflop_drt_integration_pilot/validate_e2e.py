"""End-to-end validation of the FlipFlop consistency test: raw data -> network/demand -> simulation ->
evaluation -> key figures -> every figure quoted in the READMEs, notebooks and the report.

Levels
  quick  (~1 min, run by the git pre-commit hook)
         0. the repository can be read: every tracked .md/.ipynb renders like on GitHub without visible
            raw markup, and every relative link/image points to a tracked file   (check_readability.py)
         1. unit tests (tests/)
         2. simulation results on disk are exactly the ones recorded by the last full validation, and
            inputs + simulation code are unchanged since then            (results/simulation_manifest.json)
         3. re-evaluating the results reproduces results/v2_evaluation.csv byte for byte
         4. re-computing all key figures reproduces results/key_figures.json (figures + input hashes)
         5. every quoted figure in README/notebooks/report matches key_figures.json, and the documents
            render cleanly like on GitHub (pandoc, GFM; no visible tags, no broken links)   (check_claims.py)
  full   (1.5-3 h with --parallel 5) everything in quick, plus
         a. rebuild network and demand, byte-compare with the files in data/ (restored if they differ)
         b. re-simulate every scenario of the sweep under a temporary name and compare it with the
            stored result (all 1_user-stats.csv values must be identical)
         c. re-execute the three current notebooks and compare their text outputs with the stored ones
         d. on success: write results/simulation_manifest.json

After an intended change (new data, new code, new scenarios):
  run the sweep (run_v2.py), evaluate_v2.py, key_figures.py --write, check_claims.py --update,
  re-read the changed text, then validate_e2e.py --level full.

Usage (from repo root):
  python studies/flipflop_drt_integration_pilot/validate_e2e.py                 # quick
  python studies/flipflop_drt_integration_pilot/validate_e2e.py --level full    # full, 1.5-3 h
Exit code 0 only if every step passed; steps that could not run count as failures.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

STUDY_DIR = Path(__file__).resolve().parent
ROOT_DIR = STUDY_DIR.parents[1]
RESULTS_DIR = STUDY_DIR / "results"
MANIFEST_FILE = RESULTS_DIR / "simulation_manifest.json"
SWEEP_FILES = [STUDY_DIR / "scenarios" / n for n in ("scenario_cfg_v2_sweep.csv", "scenario_cfg_v2_sweep_wait6.csv")]
NOTEBOOKS = ["flipflop_consistency_test", "consortium_presentation_flipflop_validation", "flipflop_demand_model_validity"]
PY = sys.executable

sys.path.insert(0, str(STUDY_DIR))
import key_figures as kf  # noqa: E402

GENERATED_DATA = [kf.NETWORK_DIR, kf.INIT_DIST_DIR, ROOT_DIR / "data" / "demand" / "flipflop_v2"]


# ----------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.rows = []

    def add(self, step, ok, detail=""):
        self.rows.append((step, ok, detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {step}" + (f" — {detail}" if detail else ""), flush=True)
        return ok

    @property
    def ok(self):
        return all(ok for _, ok, _ in self.rows)


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True, **kw)


def sweep_scenarios():
    return pd.concat([pd.read_csv(f) for f in SWEEP_FILES], ignore_index=True)


def simulation_code_files():
    """Code and configuration that determine the simulation results (not the documentation tooling)."""
    files = sorted(p for p in (ROOT_DIR / "src").rglob("*") if p.is_file() and p.suffix in {".py", ".pyx", ".cpp", ".h", ".hpp"}
                   and "__pycache__" not in p.parts)
    files += [ROOT_DIR / "run_examples.py", STUDY_DIR / "run_v2.py", STUDY_DIR / "build_gip_network.py",
              STUDY_DIR / "prepare_demand_v2.py", STUDY_DIR / "scenarios" / "const_cfg_v2_consistency.yaml", *SWEEP_FILES,
              ROOT_DIR / "data" / "vehicles" / "default_vehtype.csv"]
    return [f for f in files if f.is_file()]


def fingerprint(files):
    h = hashlib.sha256()
    for f in files:
        h.update(str(f.relative_to(ROOT_DIR)).encode())
        h.update(kf.sha256(f).encode())
    return h.hexdigest()


def simulation_inputs():
    return {str(f.relative_to(ROOT_DIR)): kf.sha256(f) for f in kf.input_files() if f != kf.EVALUATION_FILE}


def result_hashes(names):
    out = {}
    for s in names:
        f = RESULTS_DIR / s / "1_user-stats.csv"
        out[s] = kf.sha256(f) if f.exists() else None
    return out


# ----------------------------------------------------------------------------------------------
# quick steps
# ----------------------------------------------------------------------------------------------
def step_unit_tests(rep):
    r = run([PY, "-m", "unittest", "discover", "-s", str(STUDY_DIR / "tests")], env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
    last = [l for l in r.stderr.strip().splitlines() if l.startswith(("Ran ", "OK", "FAILED"))]
    return rep.add("unit tests", r.returncode == 0, " / ".join(last) + ("" if r.returncode == 0 else "\n" + r.stderr[-3000:]))


def step_manifest(rep):
    if not MANIFEST_FILE.exists():
        return rep.add("results match last full validation", False, f"{MANIFEST_FILE.name} missing — run --level full")
    man = json.loads(MANIFEST_FILE.read_text())
    problems = []
    if fingerprint(simulation_code_files()) != man["simulation_code_sha256"]:
        problems.append("simulation code or configuration changed")
    cur_inputs = simulation_inputs()
    problems += [f"input changed: {k}" for k, h in man["inputs_sha256"].items() if cur_inputs.get(k) != h]
    problems += [f"new input: {k}" for k in cur_inputs if k not in man["inputs_sha256"]]
    names = list(sweep_scenarios()["scenario_name"])
    if sorted(names) != sorted(man["results_sha256"]):
        problems.append("scenario list differs from the validated sweep")
    cur = result_hashes(names)
    bad = [s for s in names if cur.get(s) != man["results_sha256"].get(s)]
    if bad:
        problems.append(f"{len(bad)} result(s) missing or changed, e.g. {bad[:3]}")
    return rep.add("results match last full validation", not problems,
                   f"validated {man['validated_at']}, {len(names)} runs" if not problems else "; ".join(problems[:6]))


def step_evaluation(rep):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "eval.csv"
        r = run([PY, str(STUDY_DIR / "evaluate_v2.py"), "--pattern", "v2*", "--out", str(out)])
        if r.returncode != 0 or not out.exists():
            return rep.add("evaluation reproduces v2_evaluation.csv", False, r.stderr[-1500:])
        same = out.read_bytes() == kf.EVALUATION_FILE.read_bytes()
        return rep.add("evaluation reproduces v2_evaluation.csv", same, "" if same else "re-evaluation differs — run evaluate_v2.py and review")


def step_key_figures(rep):
    stored = json.loads(kf.KEY_FIGURES_FILE.read_text())
    figs = kf.compute()
    problems = kf.diff(figs, stored["figures"])
    cur = kf.provenance()
    problems += [f"input changed: {k}" for k, h in cur.items() if stored["inputs_sha256"].get(k) != h]
    problems += [f"input missing: {k}" for k in stored["inputs_sha256"] if k not in cur]
    return rep.add("key figures reproduce key_figures.json", not problems,
                   f"{len(figs)} figures" if not problems else "; ".join(problems[:8]))


def step_readability(rep):
    import check_readability
    errors, n = check_readability.run()
    return rep.add("repository is readable (all tracked .md/.ipynb render, links and images resolve)", not errors,
                   f"{n} documents" if not errors else "; ".join(errors[:8]))


def step_claims(rep):
    import check_claims
    errors, counts = check_claims.run()
    return rep.add("quoted figures match key figures and render correctly", not errors,
                   f"{sum(counts.values())} figures in {len(counts)} documents" if not errors else "; ".join(errors[:8]))


# ----------------------------------------------------------------------------------------------
# full steps
# ----------------------------------------------------------------------------------------------
def snapshot(dirs):
    return {str(f.relative_to(ROOT_DIR)): kf.sha256(f) for d in dirs for f in sorted(Path(d).rglob("*")) if f.is_file()}


def step_rebuild_data(rep, tmp):
    backup = Path(tmp) / "data_backup"
    for d in GENERATED_DATA:
        shutil.copytree(d, backup / d.relative_to(ROOT_DIR))
    before = snapshot(GENERATED_DATA)
    errs = []
    for script in ("build_gip_network.py", "prepare_demand_v2.py"):
        r = run([PY, str(STUDY_DIR / script)])
        if r.returncode != 0:
            errs.append(f"{script} exit {r.returncode}: {r.stderr[-800:]}")
    after = snapshot(GENERATED_DATA)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    if changed or errs:
        for d in GENERATED_DATA:  # restore the state the results were computed on
            shutil.rmtree(d)
            shutil.copytree(backup / d.relative_to(ROOT_DIR), d)
    return rep.add("network and demand rebuild byte-identical", not changed and not errs,
                   f"{len(after)} files" if not (changed or errs) else "; ".join(errs + [f"differs: {c}" for c in changed[:6]]))


def step_resimulate(rep, tmp, parallel, sample):
    sc = sweep_scenarios()
    if sample:
        sc = sc.sample(n=min(sample, len(sc)), random_state=0)
    prefix = "e2e_"
    sc_e2e = sc.copy()
    sc_e2e["scenario_name"] = prefix + sc_e2e["scenario_name"]
    # each sweep file may have its own columns (e.g. op_max_wait_time); the fleet-control default is 480 s
    if "op_max_wait_time" in sc_e2e:
        sc_e2e["op_max_wait_time"] = sc_e2e["op_max_wait_time"].fillna(480).astype(int)
    f = Path(tmp) / "e2e_scenarios.csv"
    sc_e2e.to_csv(f, index=False)
    t0 = time.time()
    r = run([PY, str(STUDY_DIR / "run_v2.py"), str(f), "--parallel", str(parallel)])
    mismatches = []
    try:
        for name in sc["scenario_name"]:
            a, b = RESULTS_DIR / name / "1_user-stats.csv", RESULTS_DIR / (prefix + name) / "1_user-stats.csv"
            if not (a.exists() and b.exists()):
                mismatches.append(f"{name}: missing result")
                continue
            da, db = pd.read_csv(a), pd.read_csv(b)
            if not da.equals(db):
                mismatches.append(f"{name}: user stats differ")
    finally:
        for name in sc["scenario_name"]:
            shutil.rmtree(RESULTS_DIR / (prefix + name), ignore_errors=True)
    detail = f"{len(sc)} runs re-simulated in {int(time.time() - t0)} s, run_v2 exit {r.returncode}"
    ok = r.returncode == 0 and not mismatches
    return rep.add("re-simulation reproduces stored results", ok, detail if ok else detail + "; " + "; ".join(mismatches[:6]))


def notebook_text_outputs(nb):
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        t = []
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream":
                t.append("".join(o["text"]))
            elif "data" in o and "text/plain" in o["data"]:
                t.append("".join(o["data"]["text/plain"]))
            elif o.get("output_type") == "error":
                t.append("ERROR " + o.get("ename", ""))
        out.append("\n".join(t))
    return out


def step_notebooks(rep, tmp):
    import nbformat
    from nbclient import NotebookClient
    problems = []
    for name in NOTEBOOKS:
        path = STUDY_DIR / "analysis" / f"{name}.ipynb"
        nb = nbformat.read(path, as_version=4)
        stored = notebook_text_outputs(nb)
        try:
            NotebookClient(nb, timeout=900, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}}).execute()
        except Exception as e:  # noqa: BLE001  (any failure is a failed validation)
            problems.append(f"{name}: {type(e).__name__}")
            continue
        nbformat.write(nb, Path(tmp) / f"{name}.executed.ipynb")
        fresh = notebook_text_outputs(nb)
        diff_cells = [i for i, (a, b) in enumerate(zip(stored, fresh)) if a != b]
        if diff_cells or len(stored) != len(fresh):
            problems.append(f"{name}: outputs of code cells {diff_cells} differ from the stored notebook")
    return rep.add("notebooks re-execute with identical outputs", not problems, "; ".join(problems))


def write_manifest():
    names = list(sweep_scenarios()["scenario_name"])
    MANIFEST_FILE.write_text(json.dumps({
        "validated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "simulation_code_sha256": fingerprint(simulation_code_files()),
        "inputs_sha256": simulation_inputs(),
        "results_sha256": result_hashes(names),
    }, indent=1, sort_keys=True) + "\n")


# ----------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--level", choices=["quick", "full"], default="quick")
    ap.add_argument("--parallel", type=int, default=5, help="simulations side by side in --level full")
    ap.add_argument("--sample", type=int, default=0,
                    help="full: re-simulate only N random scenarios (manifest is then not written)")
    args = ap.parse_args()

    rep = Report()
    print(f"FlipFlop end-to-end validation, level {args.level}", flush=True)
    step_unit_tests(rep)
    step_readability(rep)
    if args.level == "full":
        with tempfile.TemporaryDirectory() as tmp:
            step_rebuild_data(rep, tmp)
            step_resimulate(rep, tmp, args.parallel, args.sample)
            step_evaluation(rep)
            step_key_figures(rep)
            step_claims(rep)
            step_notebooks(rep, tmp)
        if rep.ok and not args.sample:
            write_manifest()
            print(f"written {MANIFEST_FILE.relative_to(ROOT_DIR)}")
        step_manifest(rep)
    else:
        step_manifest(rep)
        step_evaluation(rep)
        step_key_figures(rep)
        step_claims(rep)
    failed = [s for s, ok, _ in rep.rows if not ok]
    print(f"\n{'ALL PASSED' if not failed else 'FAILED: ' + ', '.join(failed)}  ({len(rep.rows) - len(failed)}/{len(rep.rows)} steps)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
