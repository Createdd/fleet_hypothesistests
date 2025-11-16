#!/usr/bin/env python3
"""
Reindex network to have continuous node indices (0, 1, 2, ...).
This is required by the NetworkBasic routing engine.
"""

import pandas as pd
from pathlib import Path

print("=" * 80)
print("REINDEXING NETWORK NODES")
print("=" * 80)

# Paths
NETWORK_DIR = Path("data/networks/klagenfurt_h1_spitzenzeiten/base")
ZONE_DIR = Path("data/zones/klagenfurt_h1_spitzenzeiten/base")

# Load data
print("\n[1/4] Loading network files...")
nodes = pd.read_csv(NETWORK_DIR / "nodes.csv")
edges = pd.read_csv(NETWORK_DIR / "edges.csv")
zone_info = pd.read_csv(ZONE_DIR / "node_zone_info.csv")

print(f"  Nodes: {len(nodes)}")
print(f"  Edges: {len(edges)}")
print(f"  Node index range: {nodes['node_index'].min()} - {nodes['node_index'].max()}")

# Create mapping from old to new indices
print("\n[2/4] Creating reindex mapping...")
old_to_new = {old_idx: new_idx for new_idx, old_idx in enumerate(nodes['node_index'])}
print(f"  Mapping {len(old_to_new)} nodes")

# Reindex nodes
print("\n[3/4] Reindexing nodes...")
nodes['node_index'] = nodes['node_index'].map(old_to_new)

# Reindex edges
print("  Reindexing edges...")
edges['from_node'] = edges['from_node'].map(old_to_new)
edges['to_node'] = edges['to_node'].map(old_to_new)

# Reindex zone_info
print("  Reindexing zone_info...")
zone_info['node_index'] = zone_info['node_index'].map(old_to_new)

# Save reindexed files
print("\n[4/4] Saving reindexed files...")
nodes.to_csv(NETWORK_DIR / "nodes.csv", index=False)
edges.to_csv(NETWORK_DIR / "edges.csv", index=False)
zone_info.to_csv(ZONE_DIR / "node_zone_info.csv", index=False)

print("\n" + "=" * 80)
print("REINDEXING COMPLETE")
print("=" * 80)
print(f"New node index range: {nodes['node_index'].min()} - {nodes['node_index'].max()}")
print(f"Files updated:")
print(f"  • {NETWORK_DIR / 'nodes.csv'}")
print(f"  • {NETWORK_DIR / 'edges.csv'}")
print(f"  • {ZONE_DIR / 'node_zone_info.csv'}")
print("=" * 80)
