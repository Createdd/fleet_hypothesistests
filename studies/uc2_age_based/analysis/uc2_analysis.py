import os
import glob
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY_DIR = os.path.join(ROOT_DIR)
RESULTS_DIR = os.path.join(STUDY_DIR, "results")
OUT_DIR = os.path.join(STUDY_DIR, "analysis")

os.makedirs(OUT_DIR, exist_ok=True)

# Keys we care about in standard_eval.csv
KEYS = {
    "served users [%]": "servicerate_%",
    "avg waiting time [s]": "avg_wait_s",
    "median waiting time [s]": "median_wait_s",
    "90% quant waiting time [s]": "p90_wait_s",
    "vehicle utilization [%]": "veh_util_%",
}

# Categorize scenarios by age group
AGE_GROUPS = {
    "elderly_65plus": ["baseline", "phone_support", "simple_ui", "full_support"],
    "students_15_20": ["students_15_20"],
    "students_21_30": ["students_21_30"]
}

rows = []
for scen_dir in sorted(glob.glob(os.path.join(RESULTS_DIR, "*"))):
    scen_name = os.path.basename(scen_dir)
    eval_path = os.path.join(scen_dir, "standard_eval.csv")
    if not os.path.exists(eval_path):
        continue
    df = pd.read_csv(eval_path, index_col=0)
    row = {"scenario": scen_name}

    # Determine age group
    age_group = "unknown"
    for group, scenarios in AGE_GROUPS.items():
        if scen_name in scenarios:
            age_group = group
            break
    row["age_group"] = age_group

    for k, newk in KEYS.items():
        if k in df.index:
            row[newk] = df.loc[k].values[0]
    rows.append(row)

summary = pd.DataFrame(rows).sort_values("scenario")
summary_path = os.path.join(OUT_DIR, "uc2_summary.csv")
summary.to_csv(summary_path, index=False)

print("=" * 70)
print("UC2 Analyse: Altersbasierte digitale Kompetenz und Nutzungsverhalten")
print("=" * 70)
print("\nErgebnisse nach Altersgruppe:\n")

for group, scenarios in AGE_GROUPS.items():
    group_data = summary[summary["age_group"] == group]
    if not group_data.empty:
        print(f"\n{group.upper().replace('_', ' ')}:")
        print("-" * 70)
        print(group_data.to_string(index=False))

print("\n" + "=" * 70)
print(f"Vollständige Ergebnisse gespeichert: {summary_path}")
print("=" * 70)
