import os
import multiprocessing as mp
import sys
import traceback

# Get absolute paths for macOS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from run_examples import run_scenarios
import src.misc.config as config
from src.misc.globals import *

# Set up case study path
CASE_STUDY_PATH = os.path.join(ROOT_DIR, "studies", "klagenfurt_h1_spitzenzeiten_case_study")
SC_PATH = os.path.join(CASE_STUDY_PATH, "scenarios")

if __name__ == "__main__":
    mp.freeze_support()

    try:
        # Create necessary directories
        os.makedirs(os.path.join(CASE_STUDY_PATH, "results"), exist_ok=True)
        os.makedirs(os.path.join(CASE_STUDY_PATH, "analysis"), exist_ok=True)

        # Copy vehicle file if needed
        src = os.path.join(ROOT_DIR, "data", "vehicles", "klagenfurt_peak_morning.csv")
        dst = os.path.join(ROOT_DIR, "data", "vehicles", "1.csv")
        os.makedirs(os.path.join(ROOT_DIR, "data", "vehicles"), exist_ok=True)
        if os.path.exists(src):
            import shutil
            shutil.copy(src, dst)
            print(f"Copied {os.path.basename(src)} → {os.path.basename(dst)}")

        # Run simulation
        log_level = "info"
        cc = os.path.join(SC_PATH, "const_cfg_klagenfurt_h1_spitzenzeiten_case_study.yaml")
        sc = os.path.join(SC_PATH, "scenario_cfg_klagenfurt_h1_spitzenzeiten_case_study.csv")
        run_scenarios(cc, sc, log_level=log_level, n_cpu_per_sim=1, n_parallel_sim=1)

        # Run analysis notebook
        print("\nSimulation complete. To analyze results, open:")
        print(f"studies/klagenfurt_h1_spitzenzeiten_case_study/analysis/klagenfurt_h1_spitzenzeiten_analysis.ipynb")
    except Exception as e:
        traceback.print_exc()