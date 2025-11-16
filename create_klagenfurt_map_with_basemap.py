"""
Create Klagenfurt zone map with OpenStreetMap basemap
Shows streets, buildings, and the university area with zone overlays
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
from matplotlib.patches import Patch

from shapely.geometry import Point

# 1. Load network and nodes
print("Loading network data...")
network = gpd.read_file("klagenfurt_network_extended.gpkg")  # Use extended network
nodes = pd.read_csv("data/networks/klagenfurt_h1_spitzenzeiten/base/nodes.csv")

# 2. Create GeoDataFrame from nodes (currently in WGS84)
nodes_gdf = gpd.GeoDataFrame(
    nodes,
    geometry=gpd.points_from_xy(nodes.pos_x, nodes.pos_y),
    crs="EPSG:4326"  # WGS84
)

# 3. Reproject to Web Mercator for contextily
nodes_gdf = nodes_gdf.to_crs(epsg=3857)
network = network.to_crs(epsg=3857)

# 4. Create figure
fig, ax = plt.subplots(figsize=(16, 12))

# 5. Plot network edges (streets)
network.plot(ax=ax, linewidth=0.5, color='gray', alpha=0.4, label='Straßennetzwerk')

# 6. Plot nodes colored by zone
scatter = ax.scatter(
    nodes_gdf.geometry.x,
    nodes_gdf.geometry.y,
    c=nodes_gdf['zone_id'],
    cmap='tab20',
    s=8,
    alpha=0.6,
    edgecolors='none',
    label='Knoten (farbkodiert nach Zone)'
)

# 7. Add OpenStreetMap basemap
print("Downloading OpenStreetMap basemap...")
cx.add_basemap(
    ax,
    source=cx.providers.OpenStreetMap.Mapnik,
    attribution_size=8,
    alpha=0.5
)

# 8. Set tighter axis limits to zoom in - but extend west for university
x_margin = (nodes_gdf.geometry.x.max() - nodes_gdf.geometry.x.min()) * 0.05
y_margin = (nodes_gdf.geometry.y.max() - nodes_gdf.geometry.y.min()) * 0.05

# Extend western boundary to show Lakeside Park
lakeside_lon_temp = 14.2655
lakeside_lat_temp = 46.6155
lakeside_point_temp = gpd.GeoSeries([Point(lakeside_lon_temp, lakeside_lat_temp)], crs="EPSG:4326").to_crs(epsg=3857)

# Set limits to include both network AND university
x_min = min(nodes_gdf.geometry.x.min(), lakeside_point_temp.x.values[0]) - x_margin
x_max = nodes_gdf.geometry.x.max() + x_margin
y_min = min(nodes_gdf.geometry.y.min(), lakeside_point_temp.y.values[0]) - y_margin
y_max = nodes_gdf.geometry.y.max() + y_margin

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# 9. Highlight Lakeside Park / Universität Klagenfurt
# Now within extended network bounds at actual location
lakeside_lon, lakeside_lat = 14.2655, 46.6155  # Actual Lakeside Park coordinates
lakeside_point = gpd.GeoSeries([Point(lakeside_lon, lakeside_lat)], crs="EPSG:4326").to_crs(epsg=3857)

# Add marker for university area
ax.plot(lakeside_point.x, lakeside_point.y,
        marker='*', markersize=30, color='red',
        markeredgecolor='darkred', markeredgewidth=2.5,
        label='Universität Klagenfurt / Lakeside Park', zorder=10)

# Add annotation with arrow
ax.annotate('Universität Klagenfurt\n(Lakeside Park)',
            xy=(lakeside_point.x.values[0], lakeside_point.y.values[0]),
            xytext=(30, -20), textcoords='offset points',
            fontsize=9, fontweight='bold', color='darkred',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.9, edgecolor='darkred', linewidth=1.5),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5, connectionstyle='arc3,rad=0.2'))# 10. Add zone labels
n_zones = nodes_gdf['zone_id'].nunique()
for zone_id in range(1, n_zones + 1):
    zone_nodes = nodes_gdf[nodes_gdf['zone_id'] == zone_id]
    if len(zone_nodes) > 0:
        centroid_x = zone_nodes.geometry.x.mean()
        centroid_y = zone_nodes.geometry.y.mean()
        ax.text(
            centroid_x, centroid_y, f'Zone {zone_id}',
            fontsize=14, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black', linewidth=1.5)
        )

# 11. Add colorbar
cbar = plt.colorbar(scatter, ax=ax, label='Zone ID', shrink=0.8)
cbar.set_label('Zone ID', fontsize=12)

# 12. Styling
ax.set_title('Klagenfurt Ridepooling-Netzwerk mit 12 Zonen\n(OpenStreetMap Hintergrund)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('', fontsize=0)  # Remove axis labels (Web Mercator coords not meaningful)
ax.set_ylabel('', fontsize=0)
ax.set_xticks([])
ax.set_yticks([])
ax.grid(True, alpha=0.2, linestyle='--')

# 13. Add legend
legend_elements = [
    Patch(facecolor='gray', alpha=0.4, label=f'Straßennetzwerk ({len(nodes_gdf)} Knoten, {len(network)} Kanten)'),
    Patch(facecolor='white', alpha=0.0, label=f'{n_zones} Service-Zonen (K-Means Clustering)'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red',
               markersize=15, markeredgecolor='darkred', markeredgewidth=2,
               label='Universität Klagenfurt (Lakeside Park)'),
    Patch(facecolor='white', alpha=0.0, label='Basiskarte: © OpenStreetMap contributors')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

# 14. Add note about university
ax.text(
    0.02, 0.02,
    'UC2-Hinweis: Lakeside Park ist Fokusgebiet für Studenten-Szenarien (21-30 Jahre)',
    transform=ax.transAxes,
    fontsize=9, style='italic',
    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
)

plt.tight_layout()

# 15. Save
output_file = 'klagenfurt_zones_map_with_basemap.png'
plt.savefig(output_file, dpi=200, bbox_inches='tight')
print(f"\n✅ Karte gespeichert: {output_file}")
print(f"   - {len(nodes_gdf)} Knoten")
print(f"   - {len(network)} Straßensegmente")
print(f"   - {n_zones} Zonen")
print(f"   - OpenStreetMap Hintergrund mit Straßennamen")

plt.show()
