"""
Generate full-day demand for Klagenfurt H1 Spitzenzeiten simulation.

This script generates 500 ride requests distributed across 6 AM to 10 PM,
with 70% concentration during the peak hours (7-9 AM).

Usage:
    cd /path/to/FleetPy
    conda run -n fleetpy python data/demand/klagenfurt_h1_spitzenzeiten/generate_fullday_demand.py
"""

import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Load network nodes to get valid node IDs
nodes_df = pd.read_csv('data/networks/klagenfurt_h1_spitzenzeiten/base/nodes.csv')
valid_nodes = nodes_df['node_index'].values

# Time parameters (in seconds)
start_time = 21600  # 6 AM
peak_start = 25200  # 7 AM
peak_end = 32400    # 9 AM
end_time = 79200    # 10 PM (22:00)

# Total requests and distribution
total_requests = 500
peak_requests = int(total_requests * 0.7)  # 350 requests during 7-9 AM
off_peak_requests = total_requests - peak_requests  # 150 requests outside peak

# Generate request times
peak_times = np.random.uniform(peak_start, peak_end, peak_requests)
early_morning_times = np.random.uniform(start_time, peak_start, off_peak_requests // 2)
rest_of_day_times = np.random.uniform(peak_end, end_time, off_peak_requests - len(early_morning_times))

all_times = np.concatenate([peak_times, early_morning_times, rest_of_day_times])
all_times = np.sort(all_times)

# Generate origin-destination pairs
origins = np.random.choice(valid_nodes, size=total_requests, replace=True)
destinations = np.random.choice(valid_nodes, size=total_requests, replace=True)

# Ensure origin != destination
for i in range(total_requests):
    while destinations[i] == origins[i]:
        destinations[i] = np.random.choice(valid_nodes)

# Create demand dataframe with correct column names matching original format
demand_data = []
for i in range(total_requests):
    demand_data.append({
        'Unnamed: 0': float(i),
        'request_id': float(i),
        'rq_time': float(all_times[i]),
        'start': float(origins[i]),
        'end': float(destinations[i]),
        'earliest_pickup_time': float(all_times[i])
    })

demand_df = pd.DataFrame(demand_data)

# Save to file
output_path = 'data/demand/klagenfurt_h1_spitzenzeiten/matched/klagenfurt_h1_spitzenzeiten/demand_requests.csv'
demand_df.to_csv(output_path, index=False)

# Print summary statistics
print(f"Generated {total_requests} requests")
print(f"\nTemporal distribution:")
print(f"  6-7 AM: {len(early_morning_times)} requests ({len(early_morning_times)/total_requests*100:.1f}%)")
print(f"  7-9 AM (PEAK): {peak_requests} requests ({peak_requests/total_requests*100:.1f}%)")
print(f"  9 AM-10 PM: {len(rest_of_day_times)} requests ({len(rest_of_day_times)/total_requests*100:.1f}%)")
print(f"\nNode ID range: {origins.min():.0f} - {origins.max():.0f}")
print(f"Saved to: {output_path}")
