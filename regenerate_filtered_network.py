#!/usr/bin/env python3
"""
Complete regeneration of filtered Klagenfurt network from original GeoPackage.
This script reads the original klagenfurt_network_extended.gpkg and creates
a filtered network with only the 6 core zones.

Zones to keep: 1, 4, 6, 7, 9, 10 (remapped to 0-5)
Zones to remove: 2, 3, 5, 8, 11, 12
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
from shapely.geometry import Point, LineString
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("REGENERATING FILTERED KLAGENFURT NETWORK FROM SOURCE")
print("=" * 80)

# Configuration
GPKG_FILE = "klagenfurt_network_extended.gpkg"
ZONES_TO_KEEP = [1, 4, 6, 7, 9, 10]
ZONE_MAPPING = {1: 0, 4: 1, 6: 2, 7: 3, 9: 4, 10: 5}

OUTPUT_DIR = Path("data/networks/klagenfurt_h1_spitzenzeiten/base")
ZONE_DIR = Path("data/zones/klagenfurt_h1_spitzenzeiten/base")

# Create output directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ZONE_DIR.mkdir(parents=True, exist_ok=True)

# Step 1: Load original network from GeoPackage
print("\n[1/6] Loading original network from GeoPackage...")
try:
    gdf_nodes = gpd.read_file(GPKG_FILE, layer='nodes')
    gdf_edges = gpd.read_file(GPKG_FILE, layer='edges')
    print(f"  ✓ Loaded {len(gdf_nodes):,} nodes and {len(gdf_edges):,} edges")
except Exception as e:
    print(f"  ✗ Error loading GeoPackage: {e}")
    exit(1)

# Step 2: Filter nodes to core zones
print(f"\n[2/6] Filtering nodes to core zones {ZONES_TO_KEEP}...")
original_node_count = len(gdf_nodes)
filtered_nodes = gdf_nodes[gdf_nodes['zone_id'].isin(ZONES_TO_KEEP)].copy()
print(f"  ✓ Filtered from {original_node_count:,} to {len(filtered_nodes):,} nodes")

# Step 3: Remap zone IDs
print(f"\n[3/6] Remapping zone IDs: {ZONE_MAPPING}...")
filtered_nodes['zone_id'] = filtered_nodes['zone_id'].map(ZONE_MAPPING)
for old_zone, new_zone in ZONE_MAPPING.items():
    count = (filtered_nodes['zone_id'] == new_zone).sum()
    print(f"  Zone {old_zone} → {new_zone}: {count:,} nodes")

# Step 4: Filter edges to connect only filtered nodes
print(f"\n[4/6] Filtering edges to connect filtered nodes only...")
valid_node_indices = set(filtered_nodes['node_index'].values)
filtered_edges = gdf_edges[
    gdf_edges['from_node'].isin(valid_node_indices) &
    gdf_edges['to_node'].isin(valid_node_indices)
].copy()
print(f"  ✓ Filtered from {len(gdf_edges):,} to {len(filtered_edges):,} edges")

# Step 5: Save filtered network as CSV
print(f"\n[5/6] Saving filtered network to CSV...")

# Prepare nodes DataFrame for CSV export
nodes_csv = pd.DataFrame({
    'node_index': filtered_nodes['node_index'],
    'is_stop_only': filtered_nodes.get('is_stop_only', 0),
    'pos_x': filtered_nodes.geometry.x,
    'pos_y': filtered_nodes.geometry.y,
    'zone_id': filtered_nodes['zone_id']
})

# Prepare edges DataFrame for CSV export
edges_csv = pd.DataFrame({
    'edge_index': filtered_edges['edge_index'],
    'from_node': filtered_edges['from_node'],
    'to_node': filtered_edges['to_node'],
    'distance': filtered_edges['distance'],
    'travel_time': filtered_edges['travel_time'],
    'source_edge_id': filtered_edges.get('source_edge_id', '')
})

# Save to CSV
nodes_csv.to_csv(OUTPUT_DIR / "nodes.csv", index=False)
edges_csv.to_csv(OUTPUT_DIR / "edges.csv", index=False)
print(f"  ✓ Saved nodes.csv ({len(nodes_csv):,} rows)")
print(f"  ✓ Saved edges.csv ({len(edges_csv):,} rows)")

# Step 6: Create node_zone_info.csv with centroids
print(f"\n[6/6] Generating centroids (50 per zone, 300 total)...")

# Initialize node_zone_info
node_zone_info = pd.DataFrame({
    'node_index': filtered_nodes['node_index'],
    'zone_id': filtered_nodes['zone_id'],
    'is_centroid': 0,
    'is_boarding_node': 0
})

# Generate 50 centroids per zone using spatial distribution
from scipy.spatial.distance import cdist

centroids_per_zone = 50
all_centroids = []

for zone_id in range(6):
    zone_nodes = filtered_nodes[filtered_nodes['zone_id'] == zone_id].copy()
    if len(zone_nodes) == 0:
        continue

    # Extract coordinates
    coords = np.array([[node.x, node.y] for node in zone_nodes.geometry])
    node_indices = zone_nodes['node_index'].values

    # Use K-means-like selection: iteratively pick farthest points
    n_centroids = min(centroids_per_zone, len(zone_nodes))

    # Start with the node closest to zone mean
    mean_coord = coords.mean(axis=0, keepdims=True)
    first_idx = cdist(coords, mean_coord).argmin()
    selected_indices = [first_idx]

    # Iteratively add nodes that are farthest from existing centroids
    for _ in range(n_centroids - 1):
        selected_coords = coords[selected_indices]
        min_distances = cdist(coords, selected_coords).min(axis=1)
        next_idx = min_distances.argmax()
        selected_indices.append(next_idx)

    centroids = node_indices[selected_indices]
    all_centroids.extend(centroids)
    print(f"  Zone {zone_id}: {len(centroids)} centroids")

# Mark centroids in node_zone_info
node_zone_info.loc[node_zone_info['node_index'].isin(all_centroids), 'is_centroid'] = 1

# Save node_zone_info
node_zone_info.to_csv(ZONE_DIR / "node_zone_info.csv", index=False)
print(f"  ✓ Saved node_zone_info.csv with {len(all_centroids)} centroids")

# Summary
print("\n" + "=" * 80)
print("REGENERATION COMPLETE")
print("=" * 80)
print(f"Nodes:     {len(nodes_csv):,} (from {original_node_count:,})")
print(f"Edges:     {len(edges_csv):,} (from {len(gdf_edges):,})")
print(f"Zones:     6 (from 12)")
print(f"Centroids: {len(all_centroids)} (50 per zone)")
print(f"\nZone ID mapping: {ZONE_MAPPING}")
print(f"\nOutput files:")
print(f"  • {OUTPUT_DIR / 'nodes.csv'}")
print(f"  • {OUTPUT_DIR / 'edges.csv'}")
print(f"  • {ZONE_DIR / 'node_zone_info.csv'}")
print("=" * 80)
