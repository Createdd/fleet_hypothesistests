#!/usr/bin/env python3
"""
Analyze results from all filtered network simulations.
"""

import pandas as pd
import json
from pathlib import Path

print("=" * 100)
print("FILTERED NETWORK SIMULATION RESULTS ANALYSIS")
print("=" * 100)

studies = {
    "H1 - Standard Fleet Control": "studies/klagenfurt_h1_spitzenzeiten_case_study/results",
    "H2 - Minimum Fleet Size": "studies/klagenfurt_h2_spitzenzeiten_case_study/results",
    "UC2 - Age-Based Service": "studies/uc2_age_based/results",
    "UC3 - Accessibility": "studies/uc3_accessibility/results"
}

results_summary = []

for study_name, results_dir in studies.items():
    print(f"\n{'=' * 100}")
    print(f"{study_name}")
    print(f"{'=' * 100}")

    results_path = Path(results_dir)
    if not results_path.exists():
        print(f"  ⚠ Results directory not found: {results_dir}")
        continue

    # Find all scenario directories
    scenario_dirs = sorted([d for d in results_path.iterdir() if d.is_dir() and d.name.startswith(('klagenfurt', 'uc2', 'uc3'))])

    for scenario_dir in scenario_dirs:
        scenario_name = scenario_dir.name

        # Try to load operator stats file (naming varies)
        op_stats_file = None
        for filename in ["2-0_op-stats.csv", "1_op-stats.csv", "0_op-stats.csv"]:
            candidate = scenario_dir / filename
            if candidate.exists():
                op_stats_file = candidate
                break

        if op_stats_file and op_stats_file.exists():
            try:
                op_stats = pd.read_csv(op_stats_file, sep=";")

                # Extract key metrics
                total_requests = op_stats['nr_requests'].iloc[0] if 'nr_requests' in op_stats.columns else 'N/A'
                served_requests = op_stats['nr_served'].iloc[0] if 'nr_served' in op_stats.columns else 'N/A'

                if total_requests != 'N/A' and served_requests != 'N/A':
                    service_rate = (served_requests / total_requests * 100) if total_requests > 0 else 0
                else:
                    service_rate = 'N/A'

                avg_wait = op_stats['avg_wait'].iloc[0] if 'avg_wait' in op_stats.columns else 'N/A'
                avg_trip = op_stats['avg_trip_time'].iloc[0] if 'avg_trip_time' in op_stats.columns else 'N/A'
                fleet_size = op_stats['nr_vehicles'].iloc[0] if 'nr_vehicles' in op_stats.columns else 'N/A'

                print(f"\n  {scenario_name}:")
                print(f"    Fleet Size:      {fleet_size}")
                print(f"    Total Requests:  {total_requests}")
                print(f"    Served:          {served_requests}")
                if service_rate != 'N/A':
                    print(f"    Service Rate:    {service_rate:.1f}%")
                else:
                    print(f"    Service Rate:    {service_rate}")
                if avg_wait != 'N/A':
                    print(f"    Avg Wait Time:   {avg_wait/60:.1f} min")
                else:
                    print(f"    Avg Wait Time:   {avg_wait}")
                if avg_trip != 'N/A':
                    print(f"    Avg Trip Time:   {avg_trip/60:.1f} min")
                else:
                    print(f"    Avg Trip Time:   {avg_trip}")

                results_summary.append({
                    'Study': study_name,
                    'Scenario': scenario_name,
                    'Fleet Size': fleet_size,
                    'Total Requests': total_requests,
                    'Served': served_requests,
                    'Service Rate (%)': f"{service_rate:.1f}" if service_rate != 'N/A' else service_rate,
                    'Avg Wait (min)': f"{avg_wait/60:.1f}" if avg_wait != 'N/A' else avg_wait,
                    'Avg Trip (min)': f"{avg_trip/60:.1f}" if avg_trip != 'N/A' else avg_trip
                })

            except Exception as e:
                print(f"  ⚠ Error reading {op_stats_file}: {e}")
        else:
            print(f"  ⚠ No operator stats file found in {scenario_dir}")

# Create summary table
print(f"\n{'=' * 100}")
print("SUMMARY TABLE")
print(f"{'=' * 100}\n")

if results_summary:
    summary_df = pd.DataFrame(results_summary)
    print(summary_df.to_string(index=False))

    # Save to CSV
    output_file = "filtered_network_results_summary.csv"
    summary_df.to_csv(output_file, index=False)
    print(f"\n✓ Saved summary to: {output_file}")
else:
    print("No results found")

print("\n" + "=" * 100)
