import os
import sys
import traceback
from typing import Dict, List

import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root (this script lives in studies/klagenfurt_8sitzer_studie/)
sys.path.append(ROOT_DIR)

from run_examples import run_scenarios


def build_variants(base_df: pd.DataFrame) -> pd.DataFrame:
    variants: List[pd.DataFrame] = []

    # Baseline trips
    base_trips = base_df.copy()
    base_trips["scenario_name"] = base_trips["scenario_name"].astype(str) + "__trips"
    base_trips["rq_file"] = "demand_requests_trips.csv"
    variants.append(base_trips)

    # Service constraint: stricter max wait
    svc = base_df.copy()
    svc["scenario_name"] = svc["scenario_name"].astype(str) + "__trips__svc_wait_300"
    svc["rq_file"] = "demand_requests_trips.csv"
    svc["op_max_wait_time"] = 300
    svc["op_max_detour_time_factor"] = 40
    variants.append(svc)

    # Repositioning: Basic
    repo = base_df.copy()
    repo["scenario_name"] = repo["scenario_name"].astype(str) + "__trips__repo_basic"
    repo["rq_file"] = "demand_requests_trips.csv"
    repo["op_repo_method"] = "Basic"
    variants.append(repo)

    out = pd.concat(variants, ignore_index=True)
    return out


def run_study(case_study_path: str, const_cfg: str, base_scenarios: str) -> None:
    sc_path = os.path.join(case_study_path, "scenarios")
    os.makedirs(os.path.join(case_study_path, "results"), exist_ok=True)
    os.makedirs(os.path.join(case_study_path, "analysis"), exist_ok=True)

    base_df = pd.read_csv(base_scenarios)
    out_df = build_variants(base_df)

    out_csv = os.path.join(sc_path, "_autogen_moia_minimal_variants.csv")
    out_df.to_csv(out_csv, index=False)

    run_scenarios(const_cfg, out_csv, log_level="info", n_cpu_per_sim=1, n_parallel_sim=1)


if __name__ == "__main__":
    try:
        studies: Dict[str, Dict[str, str]] = {
            "h1": {
                "case_study": os.path.join(ROOT_DIR, "studies", "klagenfurt_h1_spitzenzeiten_case_study"),
                "const_cfg": os.path.join(
                    ROOT_DIR,
                    "studies",
                    "klagenfurt_h1_spitzenzeiten_case_study",
                    "scenarios",
                    "const_cfg_klagenfurt_h1_spitzenzeiten_case_study.yaml",
                ),
                "scenarios": os.path.join(
                    ROOT_DIR,
                    "studies",
                    "klagenfurt_h1_spitzenzeiten_case_study",
                    "scenarios",
                    "scenario_cfg_klagenfurt_h1_spitzenzeiten_case_study.csv",
                ),
            },
            "h2": {
                "case_study": os.path.join(ROOT_DIR, "studies", "klagenfurt_h2_spitzenzeiten_case_study"),
                "const_cfg": os.path.join(
                    ROOT_DIR,
                    "studies",
                    "klagenfurt_h2_spitzenzeiten_case_study",
                    "scenarios",
                    "const_cfg_klagenfurt_h2_spitzenzeiten_case_study.yaml",
                ),
                "scenarios": os.path.join(
                    ROOT_DIR,
                    "studies",
                    "klagenfurt_h2_spitzenzeiten_case_study",
                    "scenarios",
                    "scenario_cfg_klagenfurt_h2_spitzenzeiten_case_study.csv",
                ),
            },
            "uc2": {
                "case_study": os.path.join(ROOT_DIR, "studies", "uc2_age_based"),
                "const_cfg": os.path.join(ROOT_DIR, "studies", "uc2_age_based", "scenarios", "const_cfg_uc2.yaml"),
                "scenarios": os.path.join(ROOT_DIR, "studies", "uc2_age_based", "scenarios", "uc2_scenarios.csv"),
            },
            "uc3": {
                "case_study": os.path.join(ROOT_DIR, "studies", "uc3_accessibility"),
                "const_cfg": os.path.join(ROOT_DIR, "studies", "uc3_accessibility", "scenarios", "const_cfg_uc3.yaml"),
                "scenarios": os.path.join(ROOT_DIR, "studies", "uc3_accessibility", "scenarios", "uc3_scenarios.csv"),
            },
        }

        for name, cfg in studies.items():
            print("\n" + "=" * 70)
            print(f"Running MOIA minimal variants for {name}")
            print("=" * 70)
            run_study(cfg["case_study"], cfg["const_cfg"], cfg["scenarios"])

        print("\nAll minimal runs completed.")
    except Exception:
        traceback.print_exc()
