import pandas as pd
import geopandas as gpd

# Load nodes
nodes = pd.read_csv("data/networks/klagenfurt_h1_spitzenzeiten/base/nodes.csv")

print("Network bounds (WGS84):")
print(f"Longitude: {nodes.pos_x.min():.4f} to {nodes.pos_x.max():.4f}")
print(f"Latitude: {nodes.pos_y.min():.4f} to {nodes.pos_y.max():.4f}")
print(f"\nCenter: {nodes.pos_x.mean():.4f}, {nodes.pos_y.mean():.4f}")

# Lakeside Park coordinates
lakeside_lon, lakeside_lat = 14.2655, 46.6155
print(f"\nLakeside Park: {lakeside_lon}, {lakeside_lat}")

# Check if within bounds
if (nodes.pos_x.min() <= lakeside_lon <= nodes.pos_x.max() and
    nodes.pos_y.min() <= lakeside_lat <= nodes.pos_y.max()):
    print("✅ Lakeside Park IS within network bounds")
else:
    print("❌ Lakeside Park is OUTSIDE network bounds")

# Find closest node to Lakeside Park
distances = ((nodes.pos_x - lakeside_lon)**2 + (nodes.pos_y - lakeside_lat)**2)**0.5
closest_idx = distances.idxmin()
closest_node = nodes.loc[closest_idx]
print(f"\nClosest node to Lakeside Park:")
print(f"  Node {closest_node.node_index}: ({closest_node.pos_x:.4f}, {closest_node.pos_y:.4f})")
print(f"  Distance: {distances.min():.4f} degrees (~{distances.min()*111:.1f} km)")
