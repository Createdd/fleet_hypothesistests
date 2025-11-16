#!/usr/bin/env python3
"""
Filter Klagenfurt network to 6 core zones and regenerate all derived data.
Reads original 6,394-node network from git history and creates filtered network.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.spatial.distance import cdist

print("=" * 80)
print("FILTERING KLAGENFURT NETWORK TO CORE ZONES")
print("=" * 80)

# Configuration
ZONES_TO_KEEP = [1, 4, 6, 7, 9, 10]
ZONE_MAPPING = {1: 0, 4: 1, 6: 2, 7: 3, 9: 4, 10: 5}
CENTROIDS_PER_ZONE = 50

# Paths
ORIGINAL_NODES = "/tmp/original_nodes.csv"
ORIGINAL_EDGES = "/tmp/original_edges.csv"
ORIGINAL_ZONE_INFO = "/tmp/original_node_zone_info.csv"

OUTPUT_DIR = Path("data/networks/klagenfurt_h1_spitzenzeiten/base")
ZONE_DIR = Path("data/zones/klagenfurt_h1_spitzenzeiten/base")

# Step 1: Load original data
print("\n[1/5] Loading original network from git history...")
nodes = pd.read_csv(ORIGINAL_NODES)
edges = pd.read_csv(ORIGINAL_EDGES)
zone_info = pd.read_csv(ORIGINAL_ZONE_INFO)
print(f"  ✓ Loaded {len(nodes):,} nodes, {len(edges):,} edges")
print(f"  ✓ Original zones: {sorted(nodes['zone_id'].unique())}")

# Step 2: Filter nodes to core zones
print(f"\n[2/5] Filtering nodes to zones {ZONES_TO_KEEP}...")
filtered_nodes = nodes[nodes['zone_id'].isin(ZONES_TO_KEEP)].copy()
print(f"  ✓ Kept {len(filtered_nodes):,} nodes (from {len(nodes):,})")

# Step 3: Remap zone IDs in nodes
print(f"\n[3/5] Remapping zone IDs: {ZONE_MAPPING}...")
filtered_nodes['zone_id'] = filtered_nodes['zone_id'].map(ZONE_MAPPING)
for new_zone in range(6):
    count = (filtered_nodes['zone_id'] == new_zone).sum()
    print(f"  Zone {new_zone}: {count:,} nodes")

# Step 4: Filter edges
print(f"\n[4/5] Filtering edges...")
valid_nodes = set(filtered_nodes['node_index'].values)
filtered_edges = edges[
    edges['from_node'].isin(valid_nodes) &
    edges['to_node'].isin(valid_nodes)
].copy()
print(f"  ✓ Kept {len(filtered_edges):,} edges (from {len(edges):,})")

# Step 5: Create node_zone_info with centroids
print(f"\n[5/5] Generating {CENTROIDS_PER_ZONE} centroids per zone...")

# Initialize node_zone_info
new_zone_info = pd.DataFrame({
    'node_index': filtered_nodes['node_index'],
    'zone_id': filtered_nodes['zone_id'],
    'is_centroid': 0,
    'is_boarding_node': 0
})

# Generate centroids using spatial distribution
all_centroids = []

for zone_id in range(6):
    zone_nodes = filtered_nodes[filtered_nodes['zone_id'] == zone_id].copy()
    if len(zone_nodes) == 0:
        print(f"  ⚠ Zone {zone_id}: No nodes!")
        continue

    # Extract coordinates
    coords = np.array(list(zip(zone_nodes['pos_x'], zone_nodes['pos_y'])))
    node_indices = zone_nodes['node_index'].values

    # Select centroids: iteratively pick farthest points
    n_centroids = min(CENTROIDS_PER_ZONE, len(zone_nodes))

    # Start with node closest to zone center
    mean_coord = coords.mean(axis=0, keepdims=True)
    first_idx = cdist(coords, mean_coord).argmin()
    selected_indices = [first_idx]

    # Iteratively add nodes farthest from existing centroids
    for _ in range(n_centroids - 1):
        selected_coords = coords[selected_indices]
        min_distances = cdist(coords, selected_coords).min(axis=1)
        next_idx = min_distances.argmax()
        selected_indices.append(next_idx)

    centroids = node_indices[selected_indices]
    all_centroids.extend(centroids)
    print(f"  Zone {zone_id}: {len(centroids)} centroids")

# Mark centroids
new_zone_info.loc[new_zone_info['node_index'].isin(all_centroids), 'is_centroid'] = 1

# Save all files
print(f"\nSaving filtered network...")
filtered_nodes.to_csv(OUTPUT_DIR / "nodes.csv", index=False)
filtered_edges.to_csv(OUTPUT_DIR / "edges.csv", index=False)
new_zone_info.to_csv(ZONE_DIR / "node_zone_info.csv", index=False)

print("\n" + "=" * 80)
print("FILTERING COMPLETE")
print("=" * 80)
print(f"Nodes:     {len(filtered_nodes):,}")
print(f"Edges:     {len(filtered_edges):,}")
print(f"Zones:     6 (remapped {ZONES_TO_KEEP} → 0-5)")
print(f"Centroids: {len(all_centroids)}")
print(f"\nFiles saved:")
print(f"  • {OUTPUT_DIR / 'nodes.csv'}")
print(f"  • {OUTPUT_DIR / 'edges.csv'}")
print(f"  • {ZONE_DIR / 'node_zone_info.csv'}")
print("=" * 80)
