import os
import multiprocessing as mp
import sys
import traceback

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from run_examples import run_scenarios

CASE_STUDY_PATH = os.path.join(ROOT_DIR, "studies", "uc2_age_based")
SC_PATH = os.path.join(CASE_STUDY_PATH, "scenarios")

if __name__ == "__main__":
    mp.freeze_support()

    try:
        os.makedirs(os.path.join(CASE_STUDY_PATH, "results"), exist_ok=True)
        os.makedirs(os.path.join(CASE_STUDY_PATH, "analysis"), exist_ok=True)

        log_level = "info"
        cc = os.path.join(SC_PATH, "const_cfg_uc2.yaml")
        sc = os.path.join(SC_PATH, "uc2_scenarios.csv")

        print("\n" + "="*70)
        print("UC2: Altersbasierte digitale Kompetenz und Nutzungsverhalten")
        print("="*70)
        print("Teil A - Ältere (65+): baseline, phone_support, simple_ui, full_support")
        print("Teil B - Schüler (15-20): students_15_20")
        print("Teil B - Studenten (21-30): students_21_30")
        print("="*70 + "\n")

        run_scenarios(cc, sc, log_level=log_level, n_cpu_per_sim=1, n_parallel_sim=1)

        print("\nSimulation abgeschlossen. Siehe Ergebnisse unter:")
        print(os.path.join(CASE_STUDY_PATH, "results"))
    except Exception:
        traceback.print_exc()
