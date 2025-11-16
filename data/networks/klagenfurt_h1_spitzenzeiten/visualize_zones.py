#!/usr/bin/env python3
"""
Visualize Klagenfurt filtered zones on OpenStreetMap basemap.

This script creates a map showing:
- OpenStreetMap basemap background
- Network nodes (colored by zone)
- Zone boundaries (convex hull)
- Centroids (marked with stars)
- Lakeside Park / Universität Klagenfurt area highlighted
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.spatial import ConvexHull
import geopandas as gpd
from shapely.geometry import Point, Polygon
import contextily as ctx
from matplotlib.patches import Rectangle

# Configuration
NETWORK_DIR = Path(__file__).parent / "base"
ZONES_DIR = Path(__file__).parent.parent.parent / "zones" / "klagenfurt_h1_spitzenzeiten" / "base"
OUTPUT_FILE = Path(__file__).parent.parent.parent.parent / "klagenfurt_filtered_zones_map.png"

print("=" * 80)
print("VISUALIZING KLAGENFURT FILTERED ZONES")
print("=" * 80)

# Load data
print("\n1. Loading network and zones...")
nodes_df = pd.read_csv(NETWORK_DIR / "nodes.csv")
zones_df = pd.read_csv(ZONES_DIR / "node_zone_info.csv")
edges_df = pd.read_csv(NETWORK_DIR / "edges.csv")

# Merge to get coordinates with zone info
merged = zones_df.merge(nodes_df[['node_index', 'pos_x', 'pos_y']], on='node_index')

print(f"   Nodes: {len(nodes_df)}")
print(f"   Zones: {zones_df['zone_id'].nunique()}")
print(f"   Centroids: {zones_df['is_centroid'].sum()}")

# Convert to GeoDataFrame with proper CRS (WGS84 lat/lon)
print("\n2. Converting to geographic coordinates...")
geometry = [Point(xy) for xy in zip(merged['pos_x'], merged['pos_y'])]
gdf = gpd.GeoDataFrame(merged, geometry=geometry, crs='EPSG:4326')

# Transform to Web Mercator for contextily
gdf_web = gdf.to_crs(epsg=3857)

# Also transform nodes for edges
nodes_gdf = gpd.GeoDataFrame(
    nodes_df,
    geometry=[Point(xy) for xy in zip(nodes_df['pos_x'], nodes_df['pos_y'])],
    crs='EPSG:4326'
).to_crs(epsg=3857)

print(f"   Lat/Lon range: X({merged['pos_x'].min():.4f}, {merged['pos_x'].max():.4f}), Y({merged['pos_y'].min():.4f}, {merged['pos_y'].max():.4f})")
print(f"   Web Mercator: X({gdf_web.geometry.x.min():.0f}, {gdf_web.geometry.x.max():.0f}), Y({gdf_web.geometry.y.min():.0f}, {gdf_web.geometry.y.max():.0f})")

# Create figure
print("\n3. Creating visualization with OpenStreetMap basemap...")
fig, ax = plt.subplots(figsize=(20, 16))

# Define colors for zones (bright, distinguishable colors)
colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C']
zone_labels = {
    0: 'Zone 0 (Core)',
    1: 'Zone 1 (East)',
    2: 'Zone 2 (South)',
    3: 'Zone 3 (West)',
    4: 'Zone 4 (North)',
    5: 'Zone 5 (University/Lakeside)'
}

# Plot zones with boundaries
print("\n4. Plotting zones and boundaries...")
for zone_id in sorted(gdf_web['zone_id'].unique()):
    zone_data = gdf_web[gdf_web['zone_id'] == zone_id]

    # Plot all nodes
    regular_nodes = zone_data[zone_data['is_centroid'] == 0]
    centroid_nodes = zone_data[zone_data['is_centroid'] == 1]

    # Regular nodes (small dots)
    ax.scatter(regular_nodes.geometry.x, regular_nodes.geometry.y,
              c=colors[zone_id], s=20, alpha=0.5, label=zone_labels[zone_id],
              edgecolors='white', linewidths=0.5, zorder=3)

    # Centroid nodes (stars)
    ax.scatter(centroid_nodes.geometry.x, centroid_nodes.geometry.y,
              c=colors[zone_id], s=200, marker='*',
              edgecolors='black', linewidths=1, alpha=1.0, zorder=5)

    # Draw zone boundary (convex hull)
    if len(zone_data) >= 3:
        points = np.column_stack([zone_data.geometry.x, zone_data.geometry.y])
        try:
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            # Close the polygon
            hull_points = np.vstack([hull_points, hull_points[0]])
            ax.plot(hull_points[:, 0], hull_points[:, 1],
                   c=colors[zone_id], linewidth=3, alpha=0.8, zorder=4)
            # Fill with transparency
            ax.fill(hull_points[:, 0], hull_points[:, 1],
                   c=colors[zone_id], alpha=0.1, zorder=1)
        except:
            pass

# Add sample of edges for network context
print("\n5. Adding network edges...")
edge_sample = edges_df.sample(n=min(300, len(edges_df)), random_state=42)
for _, edge in edge_sample.iterrows():
    from_node = nodes_gdf[nodes_gdf['node_index'] == edge['from_node']]
    to_node = nodes_gdf[nodes_gdf['node_index'] == edge['to_node']]
    if not from_node.empty and not to_node.empty:
        ax.plot([from_node.geometry.x.iloc[0], to_node.geometry.x.iloc[0]],
               [from_node.geometry.y.iloc[0], to_node.geometry.y.iloc[0]],
               c='gray', linewidth=0.5, alpha=0.3, zorder=2)

# Add OpenStreetMap basemap
print("\n6. Adding OpenStreetMap basemap...")
try:
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.6, zorder=0)
    print("   ✓ Basemap added successfully")
except Exception as e:
    print(f"   ⚠ Could not add basemap: {e}")
    print("   Continuing without basemap...")

# Highlight Lakeside/University area (approximate location - Zone 5)
university_zone = gdf_web[gdf_web['zone_id'] == 5]
if not university_zone.empty:
    center_x = university_zone.geometry.x.mean()
    center_y = university_zone.geometry.y.mean()

    # Add text annotation
    ax.annotate('Lakeside Park /\nUniversität Klagenfurt',
               xy=(center_x, center_y),
               xytext=(center_x + 1000, center_y + 1000),
               fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
               arrowprops=dict(arrowstyle='->', lw=2, color='red'),
               zorder=6)

# Formatting
ax.set_xlabel('Longitude →', fontsize=14, fontweight='bold')
ax.set_ylabel('Latitude →', fontsize=14, fontweight='bold')
ax.set_title('Klagenfurt Ridepooling Service Area - Filtered Network\n' +
            '6 Core Zones (Removed outlying areas: zones 2, 3, 5, 8, 11, 12)',
            fontsize=18, fontweight='bold', pad=20)

# Legend
legend1 = ax.legend(loc='upper left', fontsize=11, framealpha=0.95,
                   title='Service Zones', title_fontsize=12)
ax.add_artist(legend1)

# Add centroid legend
from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], marker='*', color='w',
                      markerfacecolor='black', markersize=15,
                      markeredgecolor='black', markeredgewidth=1)]
legend2 = ax.legend(custom_lines, ['Centroids (pickup/dropoff points)'],
                   loc='upper right', fontsize=11, framealpha=0.95)

ax.grid(True, alpha=0.2, zorder=0)
ax.set_aspect('equal')

# Add statistics text box
stats_text = (
    f"NETWORK STATISTICS\n"
    f"{'='*25}\n"
    f"Nodes:        {len(nodes_df):,}\n"
    f"Edges:        {len(edges_df):,}\n"
    f"Zones:        {zones_df['zone_id'].nunique()}\n"
    f"Centroids:    {zones_df['is_centroid'].sum()}\n"
    f"Avg/zone:     {len(nodes_df)/zones_df['zone_id'].nunique():.0f} nodes\n"
    f"Coverage:     Core Klagenfurt\n"
    f"              + Lakeside Park"
)
ax.text(0.02, 0.02, stats_text, transform=ax.transAxes,
       fontsize=10, verticalalignment='bottom', horizontalalignment='left',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'),
       family='monospace', zorder=7)

# Add north arrow
arrow_x = 0.95
arrow_y = 0.95
ax.annotate('N', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y-0.05),
           xycoords='axes fraction', fontsize=20, fontweight='bold',
           ha='center', va='center',
           arrowprops=dict(arrowstyle='->', lw=3, color='black'),
           zorder=7)

plt.tight_layout()

# Save figure
print(f"\n7. Saving map to: {OUTPUT_FILE}")
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
print(f"   ✓ Saved: {OUTPUT_FILE}")

# Also save to analysis directory
analysis_output = Path(__file__).parent.parent.parent.parent / "studies" / "klagenfurt_h1_spitzenzeiten_case_study" / "results" / "analysis" / "klagenfurt_filtered_zones_map.png"
analysis_output.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(analysis_output, dpi=300, bbox_inches='tight', facecolor='white')
print(f"   ✓ Saved: {analysis_output}")

print("\n" + "=" * 80)
print("BASEMAP CREATED SUCCESSFULLY")
print("=" * 80)
print(f"\nView map at: {OUTPUT_FILE}")

# Display if running interactively
try:
    plt.show()
except:
    pass
