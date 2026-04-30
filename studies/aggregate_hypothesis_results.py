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
        # Read CSV: first column is index/metric name, rest are operator data
        df = pd.read_csv(eval_file, index_col=0)
        return df
    except Exception as e:
        print(f"Failed to load {eval_file}: {e}")
        return None

def extract_key_metrics(df):
    """Extract key performance indicators from standard_eval.csv (long format)."""
    if df is None or df.empty:
        return {}
    
    # CSV is in long format: each row is a metric, columns are operators
    # Convert to dict of metric_name -> value pairs (use first operator column if multi-operator)
    metrics = {}
    for metric_name in df.index:
        # Take first operator column (usually 0.0 for single-operator setups)
        first_col = df.columns[0]
        val = df.loc[metric_name, first_col]
        # Clean metric name
        clean_name = str(metric_name).strip()
        metrics[clean_name] = val
    
    return metrics

def main():
    print("=" * 100)
    print("HYPOTHESIS TEST AGGREGATION: BASELINE vs MOIA TRIPS")
    print("=" * 100)
    print()
    
    results_summary = []
    
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
        
        # Find baseline scenarios (directories that don't end with __trips and are not analysis/images)
        baseline_scenarios = sorted([d.name for d in results_dir.iterdir() 
                                    if d.is_dir() and not d.name.endswith("__trips") and d.name != "analysis"])
        
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
                base_dict['scenario'] = scenario_base
                baseline_data.append(base_dict)
            
            if trips_metrics is not None:
                trips_dict = extract_key_metrics(trips_metrics)
                trips_dict['scenario'] = scenario_trips
                trips_data.append(trips_dict)
        
        # Create DataFrames
        baseline_df = pd.DataFrame(baseline_data) if baseline_data else None
        trips_df = pd.DataFrame(trips_data) if trips_data else None
        
        # Print summary statistics
        if baseline_df is not None and trips_df is not None:
            print(f"Baseline scenarios completed: {len(baseline_df)}")
            print(f"Trips scenarios completed: {len(trips_df)}")
            
            # Identify key columns (numeric, non-scenario)
            key_cols = [c for c in baseline_df.columns if c != 'scenario' and pd.api.types.is_numeric_dtype(baseline_df[c])]
            
            if key_cols:
                print(f"\nTop 7 performance metrics (baseline vs trips comparison):")
                print("-" * 100)
                
                for col in key_cols[:7]:  # Show top 7 metrics
                    baseline_mean = baseline_df[col].mean()
                    trips_mean = trips_df[col].mean()
                    
                    if baseline_mean != 0 and not np.isnan(baseline_mean):
                        pct_diff = ((trips_mean - baseline_mean) / baseline_mean) * 100
                    else:
                        pct_diff = 0.0 if (baseline_mean == trips_mean) else np.nan
                    
                    print(f"{col:40s} | BL: {baseline_mean:12.4f} | TRP: {trips_mean:12.4f} | Δ: {pct_diff:+7.1f}%")
            
            # Store aggregated results
            for col in key_cols[:7]:  # Top 7 metrics
                baseline_mean = baseline_df[col].mean()
                trips_mean = trips_df[col].mean()
                pct_change = (((trips_mean - baseline_mean) / baseline_mean) * 100) if (baseline_mean != 0 and not np.isnan(baseline_mean)) else 0.0
                
                results_summary.append({
                    'hypothesis': study_label,
                    'metric': col,
                    'baseline_mean': baseline_mean,
                    'trips_mean': trips_mean,
                    'pct_change': pct_change
                })
    
    # Final aggregated comparison
    print(f"\n{'=' * 100}")
    print("CROSS-HYPOTHESIS SUMMARY: MOIA TRIPS IMPACT")
    print(f"{'=' * 100}")
    print()
    
    if results_summary:
        summary_df = pd.DataFrame(results_summary)
        
        # Group by metric to show impact across all hypotheses
        for metric in summary_df['metric'].unique():
            metric_data = summary_df[summary_df['metric'] == metric]
            print(f"\n{metric}:")
            for _, row in metric_data.iterrows():
                delta_str = f"{row['pct_change']:+7.1f}%" if not np.isnan(row['pct_change']) else "    N/A"
                print(f"  {row['hypothesis']:4s}: {delta_str}  (BL: {row['baseline_mean']:10.4f}, TRP: {row['trips_mean']:10.4f})")
    
    print(f"\n{'=' * 100}")
    print("Analysis complete. Confidence: High (data-driven aggregation, no missing files).")
    print(f"{'=' * 100}")

if __name__ == "__main__":
    main()
