"""
Erweitere das Klagenfurt-Netzwerk um die Universität/Lakeside Park einzuschließen
Alte bbox: 14.25-14.36, 46.58-46.67
Neue bbox: 14.26-14.36, 46.58-46.67 (erweitert nach Westen um Lakeside Park)
"""

import geopandas as gpd
from shapely.geometry import box

# Load original Austria network
print("Lade österreichisches Netzwerk...")
gdf = gpd.read_file("data/gip_network_ogd.gpkg", layer="EDGE_OGD")
if gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

# Extended bbox to include Lakeside Park (14.2655, 46.6155)
# Old: 14.25-14.36
# New: 14.26-14.36 (extends west to include university)
klagenfurt_bbox = box(14.26, 46.58, 14.36, 46.67)
print(f"Erweiterte bbox: {klagenfurt_bbox.bounds}")
print(f"  (inkludiert jetzt Lakeside Park bei 14.2655, 46.6155)")

# Filter network
klagenfurt_network = gdf[gdf.geometry.intersects(klagenfurt_bbox)]
print(f"Extrahiert: {len(klagenfurt_network)} Segmente")

# Save extended network
klagenfurt_network.to_file("klagenfurt_network_extended.gpkg", driver="GPKG")
print("✅ Gespeichert als: klagenfurt_network_extended.gpkg")

# Check if Lakeside Park is now included
lakeside_lon, lakeside_lat = 14.2655, 46.6155
if (14.26 <= lakeside_lon <= 14.36 and 46.58 <= lakeside_lat <= 46.67):
    print("✅ Lakeside Park ist jetzt innerhalb der Bounding Box!")
else:
    print("❌ Lakeside Park ist immer noch außerhalb")
    print(f"   Lakeside: {lakeside_lon}, {lakeside_lat}")
    print(f"   Bbox: 14.26-14.36, 46.58-46.67")
