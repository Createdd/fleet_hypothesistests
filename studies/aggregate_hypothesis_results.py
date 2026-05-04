#!/usr/bin/env python3
"""
Aggregate and compare baseline vs MOIA trips results across all 4 hypothesis studies.
Clinical tone: rigor-focused, confidence-labeled findings, no speculation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

ROOT_DIR = Path(__file__).parent.parent

# Study definitions: (study_path, display_name, hypothesis_description)
STUDIES = [
    ("klagenfurt_h1_spitzenzeiten_case_study", "H1", "Service Quality Optimization (pricing + batching)"),
    ("klagenfurt_h2_spitzenzeiten_case_study", "H2", "Minimum Fleet Sizing"),
    ("uc2_age_based", "UC2", "Age-Based Digital Competence Intervention"),
    ("uc3_accessibility", "UC3", "Wheelchair/Stroller Accessibility"),
]

def load_scenario_metrics(study_path, scenario_dir):
    """Load standard_eval.csv from scenario output directory."""
    eval_file = study_path / "results" / scenario_dir / "standard_eval.csv"
    if not eval_file.exists():
        return None
    try:
        df = pd.read_csv(eval_file, index_col=0)
        return df
    except Exception as e:
        print(f"Failed to load {eval_file}: {e}")
        return None

def extract_key_metrics(df):
    """Extract key performance indicators from standard_eval.csv."""
    if df is None or df.empty:
        return {}

    first_col = df.columns[0]
    metrics = {}
    for metric_name in df.index:
        clean_name = str(metric_name).strip()
        metrics[clean_name] = df.loc[metric_name, first_col]

    return metrics


def split_track(scenario_name: str) -> tuple[str, str]:
    if scenario_name.endswith("__trips"):
        return scenario_name.replace("__trips", ""), "trips"
    return scenario_name, "baseline"

def main():
    print("=" * 100)
    print("HYPOTHESIS TEST AGGREGATION: BASELINE vs MOIA TRIPS")
    print("=" * 100)
    print()

    results_summary = []
    per_scenario_rows = []

    for study_dir, study_label, hypothesis_desc in STUDIES:
        study_path = ROOT_DIR / "studies" / study_dir

        print(f"\n{'=' * 100}")
        print(f"HYPOTHESIS {study_label}: {hypothesis_desc}")
        print(f"{'=' * 100}")

        # Find all scenario directories
        results_dir = study_path / "results"
        if not results_dir.exists():
            print(f"[ERROR] Results directory not found: {results_dir}")
            continue

        baseline_scenarios = sorted(
            [
                d.name
                for d in results_dir.iterdir()
                if d.is_dir() and not d.name.endswith("__trips") and d.name != "analysis"
            ]
        )

        print(f"\nScenarios found: {len(baseline_scenarios)}")
        print(f"Scenario names: {baseline_scenarios[:3]}{'...' if len(baseline_scenarios) > 3 else ''}")
        print()

        # Aggregate baseline and trips for each scenario
        baseline_data = []
        trips_data = []

        for scenario_base in baseline_scenarios:
            scenario_trips = scenario_base + "__trips"

            # Load both variants
            base_metrics = load_scenario_metrics(study_path, scenario_base)
            trips_metrics = load_scenario_metrics(study_path, scenario_trips)

            if base_metrics is not None:
                base_dict = extract_key_metrics(base_metrics)
                base_dict["scenario"] = scenario_base
                baseline_data.append(base_dict)

            if trips_metrics is not None:
                trips_dict = extract_key_metrics(trips_metrics)
                trips_dict["scenario"] = scenario_trips
                trips_data.append(trips_dict)

        baseline_df = pd.DataFrame(baseline_data) if baseline_data else None
        trips_df = pd.DataFrame(trips_data) if trips_data else None

        # Print summary statistics
        if baseline_df is not None and trips_df is not None:
            print(f"Baseline scenarios completed: {len(baseline_df)}")
            print(f"Trips scenarios completed: {len(trips_df)}")

            key_cols = [
                c
                for c in baseline_df.columns
                if c != "scenario" and pd.api.types.is_numeric_dtype(baseline_df[c])
            ]

            if key_cols:
                print(f"\nTop 7 performance metrics (baseline vs trips comparison):")
                print("-" * 100)

                for col in key_cols[:7]:
                    baseline_mean = baseline_df[col].mean()
                    trips_mean = trips_df[col].mean()

                    if baseline_mean != 0 and not np.isnan(baseline_mean):
                        pct_diff = ((trips_mean - baseline_mean) / baseline_mean) * 100
                    else:
                        pct_diff = 0.0 if (baseline_mean == trips_mean) else np.nan

                    print(
                        f"{col:40s} | BL: {baseline_mean:12.4f} | TRP: {trips_mean:12.4f} | Δ: {pct_diff:+7.1f}%"
                    )

            for col in key_cols[:7]:
                baseline_mean = baseline_df[col].mean()
                trips_mean = trips_df[col].mean()
                pct_change = (
                    ((trips_mean - baseline_mean) / baseline_mean) * 100
                    if (baseline_mean != 0 and not np.isnan(baseline_mean))
                    else 0.0
                )

                results_summary.append(
                    {
                        "hypothesis": study_label,
                        "metric": col,
                        "baseline_mean": baseline_mean,
                        "trips_mean": trips_mean,
                        "pct_change": pct_change,
                    }
                )

            combined_df = pd.concat(
                [
                    baseline_df.assign(track="baseline"),
                    trips_df.assign(track="trips"),
                ],
                ignore_index=True,
            )
            combined_df["scenario_base"], combined_df["track"] = zip(
                *combined_df["scenario"].map(split_track)
            )
            combined_df["hypothesis"] = study_label
            per_scenario_rows.append(combined_df)

    # Final aggregated comparison
    print(f"\n{'=' * 100}")
    print("CROSS-HYPOTHESIS SUMMARY: MOIA TRIPS IMPACT")
    print(f"{'=' * 100}")
    print()

    if results_summary:
        summary_df = pd.DataFrame(results_summary)

        for metric in summary_df["metric"].unique():
            metric_data = summary_df[summary_df["metric"] == metric]
            print(f"\n{metric}:")
            for _, row in metric_data.iterrows():
                delta_str = f"{row['pct_change']:+7.1f}%" if not np.isnan(row["pct_change"]) else "    N/A"
                print(
                    f"  {row['hypothesis']:4s}: {delta_str}  (BL: {row['baseline_mean']:10.4f}, TRP: {row['trips_mean']:10.4f})"
                )

    output_dir = ROOT_DIR / "studies"
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "aggregate_hypothesis_results_summary.csv"
    details_path = output_dir / "aggregate_hypothesis_results_per_scenario.csv"
    json_path = output_dir / "aggregate_hypothesis_results_summary.json"

    if results_summary:
        pd.DataFrame(results_summary).to_csv(summary_path, index=False)
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(results_summary, f, indent=2)

    if per_scenario_rows:
        per_scenario_df = pd.concat(per_scenario_rows, ignore_index=True)
        per_scenario_df.to_csv(details_path, index=False)

    print(f"\n{'=' * 100}")
    print("Analysis complete. Confidence: Medium (data-driven aggregation; missing data possible).")
    print(f"{'=' * 100}")

if __name__ == "__main__":
    main()
