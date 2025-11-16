#!/usr/bin/env python3
"""
Regenerate zone centroids for filtered Klagenfurt network.

This script:
1. Loads filtered network and zone assignments
2. Calculates centroids for each zone (spatially central nodes)
3. Marks centroid nodes in zone file
4. Saves updated zone file with centroids
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.spatial import distance_matrix

# Configuration
NETWORK_DIR = Path(__file__).parent / "base"
ZONES_DIR = Path(__file__).parent.parent.parent / "zones" / "klagenfurt_h1_spitzenzeiten" / "base"
CENTROIDS_PER_ZONE = 50  # Target number of centroids per zone

print("=" * 80)
print("REGENERATING ZONE CENTROIDS")
print("=" * 80)

# Load network and zones
print("\n1. Loading network and zones...")
nodes_df = pd.read_csv(NETWORK_DIR / "nodes.csv")
zones_df = pd.read_csv(ZONES_DIR / "node_zone_info.csv")

print(f"   Nodes: {len(nodes_df)}")
print(f"   Zones: {zones_df['zone_id'].nunique()}")

# Merge to get node coordinates with zone info
merged = zones_df.merge(nodes_df[['node_index', 'pos_x', 'pos_y']], on='node_index')

# Reset all centroids
zones_df['is_centroid'] = 0

print(f"\n2. Calculating centroids (target: {CENTROIDS_PER_ZONE} per zone)...")

for zone_id in sorted(zones_df['zone_id'].unique()):
    zone_nodes = merged[merged['zone_id'] == zone_id]
    n_nodes = len(zone_nodes)

    if n_nodes == 0:
        print(f"   Zone {zone_id}: No nodes (SKIPPED)")
        continue

    # Calculate how many centroids for this zone
    n_centroids = min(CENTROIDS_PER_ZONE, n_nodes)

    # Get node coordinates
    coords = zone_nodes[['pos_x', 'pos_y']].values

    if n_centroids >= n_nodes:
        # All nodes are centroids
        centroid_indices = zone_nodes['node_index'].values
    else:
        # Use K-means-like approach: select spatially distributed nodes
        # Start with geometric center
        center = coords.mean(axis=0)

        # Find node closest to center
        distances_to_center = np.sqrt(((coords - center) ** 2).sum(axis=1))
        centroids_idx = [np.argmin(distances_to_center)]

        # Iteratively add nodes that are furthest from existing centroids
        while len(centroids_idx) < n_centroids:
            centroid_coords = coords[centroids_idx]
            # For each non-centroid node, find min distance to any centroid
            non_centroid_mask = np.ones(len(coords), dtype=bool)
            non_centroid_mask[centroids_idx] = False

            if not non_centroid_mask.any():
                break

            non_centroid_coords = coords[non_centroid_mask]
            dists = distance_matrix(non_centroid_coords, centroid_coords)
            min_dists = dists.min(axis=1)

            # Add node with maximum minimum distance
            non_centroid_indices = np.where(non_centroid_mask)[0]
            farthest_idx = non_centroid_indices[np.argmax(min_dists)]
            centroids_idx.append(farthest_idx)

        centroid_indices = zone_nodes.iloc[centroids_idx]['node_index'].values

    # Mark centroids in zones_df
    zones_df.loc[zones_df['node_index'].isin(centroid_indices), 'is_centroid'] = 1

    print(f"   Zone {zone_id}: {n_nodes} nodes → {len(centroid_indices)} centroids")

# Save updated zones
print("\n3. Saving updated zone file...")
zones_df.to_csv(ZONES_DIR / "node_zone_info.csv", index=False)

# Print summary
total_centroids = zones_df['is_centroid'].sum()
print(f"\n4. Summary:")
print(f"   ✓ Total centroids: {total_centroids}")
print(f"   ✓ Total nodes: {len(zones_df)}")
print(f"   ✓ Centroid ratio: {total_centroids/len(zones_df)*100:.1f}%")

print("\n" + "=" * 80)
print("CENTROIDS REGENERATED")
print("=" * 80)
print("\nNext step:")
print("python ../../../demand/klagenfurt_h1_spitzenzeiten/generate_fullday_demand.py")
