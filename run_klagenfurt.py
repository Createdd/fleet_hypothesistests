import os
import shutil
from run_examples import run_scenarios

if __name__ == "__main__":
    # 1) Paths
    const_cfg = "studies/klagenfurt/klagenfurt_constant.yml"
    scen_cfg  = "studies/klagenfurt/klagenfurt_scenarios.csv"

    # 2) Ensure descriptive vehicle file is copied to numeric name
    src = os.path.join("data/vehicles", "klagenfurt_peak_morning.csv")
    dst = os.path.join("data/vehicles", "1.csv")
    os.makedirs("data/vehicles", exist_ok=True)
    shutil.copy(src, dst)
    print(f"Copied {src} → {dst}")

    # 3) Run the simulation (FleetPy will now load data/vehicles/1.csv)
    run_scenarios(const_cfg, scen_cfg, n_parallel_sim=1)