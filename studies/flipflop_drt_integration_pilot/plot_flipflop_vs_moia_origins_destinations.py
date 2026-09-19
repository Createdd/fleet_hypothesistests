from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point


ROOT_DIR = Path(__file__).resolve().parents[2]
MOIA_FILE = ROOT_DIR / "data" / "demand" / "trips_klagenfurt.csv"
FLIPFLOP_FILE = ROOT_DIR / "data" / "SampleFiles_recovered" / "SampleFiles" / "neubau" / "draws_Baseline.csv"
NETWORK_NODES = ROOT_DIR / "data" / "networks" / "klagenfurt_h1_spitzenzeiten" / "base" / "nodes.csv"
NETWORK_GEOMETRY = ROOT_DIR / "klagenfurt_network_extended.gpkg"
OUTPUT_FILE = ROOT_DIR / "studies" / "flipflop_drt_integration_pilot" / "results" / "flipflop_vs_moia_origins_destinations.png"


def main() -> None:
    moia = pd.read_csv(MOIA_FILE)
    flipflop = pd.read_csv(
        FLIPFLOP_FILE,
        usecols=["draw", "lat_start", "lon_start", "lat_end", "lon_end"],
    )
    flipflop = flipflop[flipflop["draw"] == 1]
    nodes = pd.read_csv(NETWORK_NODES)
    network = gpd.read_file(NETWORK_GEOMETRY).to_crs(epsg=3857)
    moia_origins = gpd.GeoSeries(gpd.points_from_xy(moia.origin_x, moia.origin_y), crs="EPSG:4326").to_crs(epsg=3857)
    moia_destinations = gpd.GeoSeries(gpd.points_from_xy(moia.destination_x, moia.destination_y), crs="EPSG:4326").to_crs(epsg=3857)
    flipflop_origins = gpd.GeoSeries(gpd.points_from_xy(flipflop.lon_start, flipflop.lat_start), crs="EPSG:4326").to_crs(epsg=3857)
    flipflop_destinations = gpd.GeoSeries(gpd.points_from_xy(flipflop.lon_end, flipflop.lat_end), crs="EPSG:4326").to_crs(epsg=3857)
    node_points = gpd.GeoSeries(gpd.points_from_xy(nodes.pos_x, nodes.pos_y), crs="EPSG:4326").to_crs(epsg=3857)

    fig, axes = plt.subplots(1, 2, figsize=(15, 7), sharex=True, sharey=True)
    panels = (
        (moia_origins, flipflop_origins, "Origins"),
        (moia_destinations, flipflop_destinations, "Destinations"),
    )
    for ax, (moia_points, flipflop_points, title) in zip(axes, panels):
        network.plot(ax=ax, linewidth=0.35, color="0.25", alpha=0.45, zorder=1)
        ax.scatter(node_points.x, node_points.y, s=2, color="0.7", alpha=0.25, label="FleetPy network nodes", zorder=2)
        ax.scatter(moia_points.x, moia_points.y, s=8, color="#1769aa", alpha=0.35, label="MOIA trips", zorder=3)
        ax.scatter(flipflop_points.x, flipflop_points.y, s=8, color="#d95f02", alpha=0.35, label="FlipFlop Neubau Draw 1", zorder=4)
        ax.set_title(f"{title}: MOIA vs FlipFlop")
        ax.set_axis_off()
    axes[0].legend(loc="best")
    fig.suptitle("Klagenfurt trip points on local street network: MOIA vs FlipFlop", fontsize=14)
    fig.tight_layout()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=180, bbox_inches="tight")
    print(f"MOIA trips: {len(moia)}")
    print(f"FlipFlop Draw 1 trips: {len(flipflop)}")
    print(f"Wrote: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()