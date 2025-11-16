"""
Regenerate nodes, edges, and zones from extended network (includes Lakeside Park)
This will create a new network dataset that includes the university area
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import MultiLineString, Point
from sklearn.cluster import KMeans
import os

print("=" * 70)
print("REGENERATING KLAGENFURT NETWORK WITH LAKESIDE PARK")
print("=" * 70)

# 1. Load extended network
print("\n1. Loading extended network...")
network = gpd.read_file("klagenfurt_network_extended.gpkg")
print(f"   Loaded {len(network)} street segments")

# 2. Build nodes and edges from network
print("\n2. Extracting nodes and edges from geometry...")
nodes_list = []
edges_list = []
node_id = 0
node_lookup = {}

def process_line(line):
    global node_id
    coords = list(line.coords)
    start, end = coords[0], coords[-1]
    for coord in (start, end):
        if coord not in node_lookup:
            node_lookup[coord] = node_id
            nodes_list.append({
                'node_index': node_id,
                'is_stop_only': 0,
                'pos_x': coord[0],
                'pos_y': coord[1]
            })
            node_id += 1
    o = node_lookup[start]
    d = node_lookup[end]
    length = line.length
    return o, d, length

for _, row in network.iterrows():
    geom = row.geometry
    parts = geom.geoms if isinstance(geom, MultiLineString) else [geom]
    for part in parts:
        o, d, length = process_line(part)
        dist_m = length * 111000  # Approx conversion to meters
        tt_s = max(30, dist_m / (50_000/3600))  # Travel time assuming 50 km/h
        edges_list.append({
            'from_node': o,
            'to_node': d,
            'distance': dist_m,
            'travel_time': tt_s,
            'source_edge_id': np.nan
        })

nodes_df = pd.DataFrame(nodes_list)
edges_df = pd.DataFrame(edges_list)

print(f"   ✅ Extracted {len(nodes_df)} nodes")
print(f"   ✅ Extracted {len(edges_df)} edges")
print(f"   Longitude range: {nodes_df.pos_x.min():.4f} to {nodes_df.pos_x.max():.4f}")
print(f"   Latitude range: {nodes_df.pos_y.min():.4f} to {nodes_df.pos_y.max():.4f}")

# Verify Lakeside Park is now included
lakeside_lon, lakeside_lat = 14.2655, 46.6155
if (nodes_df.pos_x.min() <= lakeside_lon <= nodes_df.pos_x.max() and 
    nodes_df.pos_y.min() <= lakeside_lat <= nodes_df.pos_y.max()):
    print(f"   ✅ Lakeside Park ({lakeside_lon}, {lakeside_lat}) IS within bounds!")
else:
    print(f"   ⚠️  Lakeside Park ({lakeside_lon}, {lakeside_lat}) still outside bounds")

# 3. Create 12 zones via K-Means clustering
print("\n3. Creating 12 zones via K-Means clustering...")
n_zones = 12
coords = nodes_df[['pos_x', 'pos_y']].values
kmeans = KMeans(n_clusters=n_zones, random_state=42).fit(coords)
nodes_df['zone_id'] = kmeans.labels_ + 1

print(f"   ✅ Created {n_zones} zones")
for zone_id in range(1, n_zones + 1):
    zone_nodes = nodes_df[nodes_df['zone_id'] == zone_id]
    print(f"   Zone {zone_id:2d}: {len(zone_nodes):4d} nodes")

# Check which zone contains Lakeside Park area
lakeside_distances = ((nodes_df.pos_x - lakeside_lon)**2 + (nodes_df.pos_y - lakeside_lat)**2)**0.5
closest_node = nodes_df.loc[lakeside_distances.idxmin()]
print(f"\n   ℹ️  Lakeside Park is closest to Zone {int(closest_node.zone_id)}")
print(f"      (Node {int(closest_node.node_index)} at {closest_node.pos_x:.4f}, {closest_node.pos_y:.4f})")

# 4. Create zone mapping with centroids
print("\n4. Creating zone mapping with centroids...")
zone_mapping = pd.DataFrame({
    'node_index': nodes_df['node_index'],
    'zone_id': nodes_df['zone_id'],
    'is_centroid': 0,
    'is_boarding_node': 1  # All nodes are boarding nodes
})

# Select centroids: nodes closest to zone centers
centroids = []
for zone_id in range(1, n_zones + 1):
    zone_nodes = nodes_df[nodes_df['zone_id'] == zone_id]
    center = kmeans.cluster_centers_[zone_id - 1]
    
    distances = np.sqrt(
        (zone_nodes['pos_x'] - center[0])**2 +
        (zone_nodes['pos_y'] - center[1])**2
    )
    
    n_centroids = max(10, len(zone_nodes) // 20)
    closest_nodes = zone_nodes.iloc[distances.argsort()[:n_centroids]]['node_index'].tolist()
    centroids.extend(closest_nodes)

zone_mapping.loc[zone_mapping['node_index'].isin(centroids), 'is_centroid'] = 1
print(f"   ✅ Selected {len(centroids)} centroids ({len(centroids)//n_zones} per zone avg)")

# 5. Save files
print("\n5. Saving network files...")
output_dir = 'data/networks/klagenfurt_h1_spitzenzeiten/base'
os.makedirs(output_dir, exist_ok=True)

nodes_df.to_csv(f'{output_dir}/nodes.csv', index=False)
edges_df.to_csv(f'{output_dir}/edges.csv', index=False)
print(f"   ✅ Saved nodes.csv ({len(nodes_df)} nodes)")
print(f"   ✅ Saved edges.csv ({len(edges_df)} edges)")

zone_dir = 'data/zones/klagenfurt_h1_spitzenzeiten/base'
os.makedirs(zone_dir, exist_ok=True)
zone_mapping.to_csv(f'{zone_dir}/node_zone_info.csv', index=False)
print(f"   ✅ Saved node_zone_info.csv ({len(zone_mapping)} mappings)")

print("\n" + "=" * 70)
print("✅ NETWORK REGENERATION COMPLETE")
print("=" * 70)
print(f"\nSummary:")
print(f"  • Nodes: {len(nodes_df):,}")
print(f"  • Edges: {len(edges_df):,}")
print(f"  • Zones: {n_zones}")
print(f"  • Centroids: {len(centroids)}")
print(f"  • Lakeside Park included: ✅")
print(f"\nNext steps:")
print(f"  1. Run: python create_klagenfurt_map_with_basemap.py")
print(f"  2. Verify Lakeside Park marker appears on map")
print(f"  3. Re-run simulations if needed (old results may be outdated)")
