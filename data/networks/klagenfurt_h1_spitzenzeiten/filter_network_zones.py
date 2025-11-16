#!/usr/bin/env python3
"""
Filter Klagenfurt network to remove outlying zones.

This script:
1. Removes zones 2, 3, 5, 8, 11, 12 (outlying areas)
2. Keeps only zones 1, 4, 6, 7, 9, 10 (core Klagenfurt)
3. Filters nodes to only those in kept zones
4. Filters edges to only connect kept nodes
5. Regenerates zone assignments with new IDs (0-5)
6. Saves filtered network and zones

Zones to REMOVE (outlying): 2, 3, 5, 8, 11, 12
Zones to KEEP (core): 1, 4, 6, 7, 9, 10
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path

# Configuration
ZONES_TO_KEEP = [1, 4, 6, 7, 9, 10]  # Core Klagenfurt zones
NETWORK_DIR = Path(__file__).parent / "base"
ZONES_DIR = Path(__file__).parent.parent.parent / "zones" / "klagenfurt_h1_spitzenzeiten" / "base"

print("=" * 80)
print("FILTERING KLAGENFURT NETWORK - REMOVING OUTLYING ZONES")
print("=" * 80)
print(f"\nZones to KEEP: {ZONES_TO_KEEP}")
print(f"Zones to REMOVE: [2, 3, 5, 8, 11, 12]")

# Load current zone assignments
print("\n1. Loading current zone assignments...")
zones_df = pd.read_csv(ZONES_DIR / "node_zone_info.csv")
print(f"   Total nodes: {len(zones_df)}")
print(f"   Unique zones: {sorted(zones_df['zone_id'].unique())}")

# Filter nodes to keep only those in selected zones
print("\n2. Filtering nodes...")
filtered_zones = zones_df[zones_df['zone_id'].isin(ZONES_TO_KEEP)].copy()
kept_nodes = set(filtered_zones['node_index'])
print(f"   Nodes after filtering: {len(filtered_zones)}")
print(f"   Removed: {len(zones_df) - len(filtered_zones)} nodes")

# Remap zone IDs to 0-5
zone_mapping = {old_id: new_id for new_id, old_id in enumerate(sorted(ZONES_TO_KEEP))}
filtered_zones['zone_id'] = filtered_zones['zone_id'].map(zone_mapping)
print(f"\n   Zone ID mapping: {zone_mapping}")

# Load and filter network files
print("\n3. Loading network files...")
nodes_df = pd.read_csv(NETWORK_DIR / "nodes.csv")
edges_df = pd.read_csv(NETWORK_DIR / "edges.csv")
print(f"   Original: {len(nodes_df)} nodes, {len(edges_df)} edges")

# Filter nodes
print("\n4. Filtering network nodes...")
filtered_nodes = nodes_df[nodes_df['node_index'].isin(kept_nodes)].copy()
print(f"   Kept: {len(filtered_nodes)} nodes")

# Filter edges - keep only if both from_node and to_node are in kept_nodes
print("\n5. Filtering network edges...")
filtered_edges = edges_df[
    edges_df['from_node'].isin(kept_nodes) &
    edges_df['to_node'].isin(kept_nodes)
].copy()
print(f"   Kept: {len(filtered_edges)} edges")
print(f"   Removed: {len(edges_df) - len(filtered_edges)} edges")

# Create backup directory
backup_dir = NETWORK_DIR / "backup_fullnetwork"
backup_dir.mkdir(exist_ok=True)

# Backup original files
print("\n6. Creating backups...")
nodes_df.to_csv(backup_dir / "nodes.csv", index=False)
edges_df.to_csv(backup_dir / "edges.csv", index=False)
zones_df.to_csv(ZONES_DIR.parent / "backup_fullnetwork_node_zone_info.csv", index=False)
print(f"   Backups saved to: {backup_dir}")

# Save filtered files
print("\n7. Saving filtered network...")
filtered_nodes.to_csv(NETWORK_DIR / "nodes.csv", index=False)
filtered_edges.to_csv(NETWORK_DIR / "edges.csv", index=False)
filtered_zones.to_csv(ZONES_DIR / "node_zone_info.csv", index=False)

print("\n8. Summary:")
print(f"   ✓ Nodes: {len(nodes_df)} → {len(filtered_nodes)}")
print(f"   ✓ Edges: {len(edges_df)} → {len(filtered_edges)}")
print(f"   ✓ Zones: 12 → {len(ZONES_TO_KEEP)}")
print(f"   ✓ Zone IDs remapped: {zone_mapping}")

# Calculate statistics per zone
print("\n9. Nodes per zone:")
for zone_id in sorted(filtered_zones['zone_id'].unique()):
    count = len(filtered_zones[filtered_zones['zone_id'] == zone_id])
    old_zone = sorted(ZONES_TO_KEEP)[zone_id]
    print(f"   Zone {zone_id} (was {old_zone}): {count} nodes")

print("\n" + "=" * 80)
print("FILTERING COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. Run: python regenerate_centroids.py")
print("2. Run: python ../../../demand/klagenfurt_h1_spitzenzeiten/generate_fullday_demand.py")
print("3. Run simulations")
