# Klagenfurt H1 Filtered Network

## Overview

This directory contains the filtered Klagenfurt network for the H1 simulation study. The network has been reduced from 12 zones to 6 core zones to improve simulation performance and focus on the central Klagenfurt area.

## Network Statistics

- **Nodes**: 3,435 (filtered from 6,394)
- **Edges**: 4,338 (filtered from 8,277)
- **Zones**: 6 (filtered from 12)
- **Centroids**: 300 (50 per zone)
- **Node Index Range**: 0-3434 (continuous, required by NetworkBasic)

## Zone Configuration

**Zones Kept** (core Klagenfurt):
- Zone 0 (was 1): 396 nodes
- Zone 1 (was 4): 669 nodes
- Zone 2 (was 6): 577 nodes
- Zone 3 (was 7): 656 nodes
- Zone 4 (was 9): 391 nodes
- Zone 5 (was 10): 746 nodes

**Zones Removed** (outlying areas): 2, 3, 5, 8, 11, 12

## Setup Process

To regenerate the filtered network from scratch:

```bash
# 1. Extract original network from git and create filtered version
cd /Users/danieldeutsch/Desktop/code_projects/FleetPy/data/networks/klagenfurt_h1_spitzenzeiten
python setup_filtered_network.py

# 2. Visualize the filtered zones
python visualize_zones.py

# 3. Generate demand for the filtered network
cd ../../demand/klagenfurt_h1_spitzenzeiten
python generate_fullday_demand.py
```

## Scripts

### `setup_filtered_network.py`
**Complete network setup in one script**
- Extracts original 6,394-node network from git history
- Filters to 6 core zones
- Remaps zone IDs to 0-5
- **Automatically reindexes nodes** to continuous 0-N range
- Reindexes edges accordingly
- Generates 300 centroids with spatial distribution
- **Single unified script** - no additional steps needed

### `visualize_zones.py`
**Creates OpenStreetMap visualization**
- Generates basemap with zone boundaries
- Shows centroid locations
- Displays network edges
- Marks Lakeside Park/University location
- Output: `klagenfurt_filtered_zones_map.png`

## Files

### Base Network Files
- `base/nodes.csv` - Node definitions (reindexed 0-3434)
- `base/edges.csv` - Edge connections (using reindexed node IDs)

### Zone Files
- `../../zones/klagenfurt_h1_spitzenzeiten/base/node_zone_info.csv` - Zone assignments and centroids

## Technical Details

### Node Reindexing
The original network has non-continuous node indices (e.g., 0, 1, 6, 7, ..., 6392). After filtering, these become even more sparse. The NetworkBasic routing engine requires continuous indices (RangeIndex), so all nodes are automatically reindexed to 0-3434.

**Mapping**: Old sparse indices → New continuous 0-N indices
- Applied to: nodes.csv, edges.csv (from_node, to_node), node_zone_info.csv

### Centroid Generation
Centroids are selected using an iterative spatial distribution algorithm:
1. Start with node closest to zone center
2. Iteratively add nodes farthest from existing centroids
3. Ensures good spatial coverage across each zone
4. 50 centroids per zone (300 total)

## Related Files

- Demand: `../../demand/klagenfurt_h1_spitzenzeiten/`
- Zones: `../../zones/klagenfurt_h1_spitzenzeiten/`
- Simulations: `../../../studies/klagenfurt_h1_spitzenzeiten_case_study/`

## Validation

After setup, verify:
```bash
# Check node count and continuous indices
head -2 base/nodes.csv && tail -2 base/nodes.csv

# Check zone distribution
cut -d, -f5 base/nodes.csv | tail -n +2 | sort -n | uniq -c

# Verify node_zone_info matches
cut -d, -f2 ../../zones/klagenfurt_h1_spitzenzeiten/base/node_zone_info.csv | tail -n +2 | sort -n | uniq -c
```

Expected output: 6 zones (0-5) with node counts matching above.
