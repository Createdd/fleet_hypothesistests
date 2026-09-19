from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
MOIA_FILE = ROOT_DIR / "data" / "demand" / "trips_klagenfurt.csv"
FLIPFLOP_FILE = ROOT_DIR / "data" / "SampleFiles_recovered" / "SampleFiles" / "neubau" / "draws_Baseline.csv"
NETWORK_NODES = ROOT_DIR / "data" / "networks" / "klagenfurt_h1_spitzenzeiten" / "base" / "nodes.csv"
NETWORK_GEOMETRY = ROOT_DIR / "klagenfurt_network_extended.gpkg"
OUTPUT_FILE = ROOT_DIR / "studies" / "flipflop_drt_integration_pilot" / "results" / "flipflop_vs_moia_with_extended_street_network.png"


def to_web_mercator(x: pd.Series, y: pd.Series) -> gpd.GeoSeries:
    return gpd.GeoSeries(gpd.points_from_xy(x, y), crs="EPSG:4326").to_crs(epsg=3857)


def main() -> None:
    moia = pd.read_csv(MOIA_FILE)
    flipflop = pd.read_csv(
        FLIPFLOP_FILE,
        usecols=["draw", "lat_start", "lon_start", "lat_end", "lon_end"],
    )
    flipflop = flipflop[flipflop["draw"] == 1]
    nodes = pd.read_csv(NETWORK_NODES)
    network = gpd.read_file(NETWORK_GEOMETRY).to_crs(epsg=3857)
    node_points = to_web_mercator(nodes["pos_x"], nodes["pos_y"])

    moia_origins = to_web_mercator(moia["origin_x"], moia["origin_y"])
    moia_destinations = to_web_mercator(moia["destination_x"], moia["destination_y"])
    flipflop_origins = to_web_mercator(flipflop["lon_start"], flipflop["lat_start"])
    flipflop_destinations = to_web_mercator(flipflop["lon_end"], flipflop["lat_end"])

    fig, ax = plt.subplots(figsize=(20, 14))
    network.plot(ax=ax, linewidth=0.4, color="#4a5568", alpha=0.65, zorder=1)
    ax.scatter(node_points.x, node_points.y, s=2, color="#718096", alpha=0.2, label="FleetPy network nodes", zorder=2)
    ax.scatter(moia_origins.x, moia_origins.y, s=18, marker="o", facecolors="none", edgecolors="#1769aa", linewidths=0.7, alpha=0.45, label="MOIA origins", zorder=3)
    ax.scatter(moia_destinations.x, moia_destinations.y, s=18, marker="x", color="#1769aa", linewidths=0.7, alpha=0.45, label="MOIA destinations", zorder=3)
    ax.scatter(flipflop_origins.x, flipflop_origins.y, s=18, marker="o", facecolors="none", edgecolors="#d95f02", linewidths=0.7, alpha=0.45, label="FlipFlop origins", zorder=4)
    ax.scatter(flipflop_destinations.x, flipflop_destinations.y, s=18, marker="x", color="#d95f02", linewidths=0.7, alpha=0.45, label="FlipFlop destinations", zorder=4)
    ax.set_title("Klagenfurt: MOIA and FlipFlop origins and destinations", fontsize=20, pad=16)
    ax.legend(loc="upper left", framealpha=0.95, ncol=2, fontsize=11)
    ax.set_axis_off()
    fig.text(0.5, 0.02, "Circle = origin | X = destination | Street geometry: klagenfurt_network_extended.gpkg | (C) OpenStreetMap contributors", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=180, bbox_inches="tight")
    print(f"MOIA trips: {len(moia)}")
    print(f"FlipFlop Draw 1 trips: {len(flipflop)}")
    print(f"Extended street segments: {len(network)}")
    print(f"Wrote: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()