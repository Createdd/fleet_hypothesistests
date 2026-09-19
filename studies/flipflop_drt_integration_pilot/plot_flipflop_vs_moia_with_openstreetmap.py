from pathlib import Path

import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
MOIA_FILE = ROOT_DIR / "data" / "demand" / "trips_klagenfurt.csv"
FLIPFLOP_FILE = ROOT_DIR / "data" / "SampleFiles_recovered" / "SampleFiles" / "neubau" / "draws_Baseline.csv"
NETWORK_NODES = ROOT_DIR / "data" / "networks" / "klagenfurt_h1_spitzenzeiten" / "base" / "nodes.csv"
NETWORK_GEOMETRY = ROOT_DIR / "klagenfurt_network_extended.gpkg"
OUTPUT_FILE = ROOT_DIR / "studies" / "flipflop_drt_integration_pilot" / "results" / "flipflop_vs_moia_with_openstreetmap.png"


def main() -> None:
    moia = pd.read_csv(MOIA_FILE)
    flipflop = pd.read_csv(
        FLIPFLOP_FILE,
        usecols=["draw", "lat_start", "lon_start", "lat_end", "lon_end"],
    )
    flipflop = flipflop[flipflop["draw"] == 1]
    nodes = pd.read_csv(NETWORK_NODES)
    network = gpd.read_file(NETWORK_GEOMETRY).to_crs(epsg=3857)

    point_sets = {
        "origins": (
            gpd.GeoSeries(gpd.points_from_xy(moia.origin_x, moia.origin_y), crs="EPSG:4326").to_crs(epsg=3857),
            gpd.GeoSeries(gpd.points_from_xy(flipflop.lon_start, flipflop.lat_start), crs="EPSG:4326").to_crs(epsg=3857),
        ),
        "destinations": (
            gpd.GeoSeries(gpd.points_from_xy(moia.destination_x, moia.destination_y), crs="EPSG:4326").to_crs(epsg=3857),
            gpd.GeoSeries(gpd.points_from_xy(flipflop.lon_end, flipflop.lat_end), crs="EPSG:4326").to_crs(epsg=3857),
        ),
    }
    node_points = gpd.GeoSeries(gpd.points_from_xy(nodes.pos_x, nodes.pos_y), crs="EPSG:4326").to_crs(epsg=3857)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharex=True, sharey=True)
    for ax, (title, (moia_points, flipflop_points)) in zip(axes, point_sets.items()):
        network.plot(ax=ax, linewidth=0.45, color="#3f4b52", alpha=0.65, zorder=1)
        ax.scatter(node_points.x, node_points.y, s=2, color="#6c757d", alpha=0.25, label="FleetPy network nodes", zorder=2)
        ax.scatter(moia_points.x, moia_points.y, s=9, color="#1769aa", alpha=0.45, label="MOIA trips", zorder=3)
        ax.scatter(flipflop_points.x, flipflop_points.y, s=9, color="#d95f02", alpha=0.45, label="FlipFlop Neubau Draw 1", zorder=4)
        cx.add_basemap(ax, source=cx.providers.OpenStreetMap.HOT, attribution_size=7, alpha=0.7, reset_extent=False)
        ax.set_title(f"{title.title()}: MOIA vs FlipFlop")
        ax.set_axis_off()

    axes[0].legend(loc="upper left", framealpha=0.9)
    fig.suptitle("Klagenfurt trip points on OpenStreetMap: MOIA vs FlipFlop", fontsize=15)
    fig.tight_layout()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=180, bbox_inches="tight")
    print(f"MOIA trips: {len(moia)}")
    print(f"FlipFlop Draw 1 trips: {len(flipflop)}")
    print(f"Wrote: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()