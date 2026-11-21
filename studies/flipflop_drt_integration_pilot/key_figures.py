"""Single source of truth for every result figure quoted in the READMEs, notebooks and report.

Every number that the documentation states as a result is computed here from the raw inputs and
the simulation results, and written to results/key_figures.json together with SHA-256 hashes of
all inputs (provenance). check_claims.py compares the documentation against this file;
validate_e2e.py runs the whole chain.

Definitions (one demand basis everywhere: the v2 demand that is simulated):
  * service area   = MOIA coordinate frame (min/max of all MOIA origins and destinations)
  * switcher       = trip that is not PT in draws_Baseline.csv but PT in draws_DRT_Kostenx1.csv
                     (same draw, same trip_id), full 24 h day, all five draws
  * zone figures   = switcher origins vs. all real MOIA origins on the 8 MOIA-derived zones
  * fleet figures  = results/v2_evaluation.csv, probe runs excluded; "standard" = max. 8 min wait,
                     "w6" = service configured to the assumed level of service (max. 6.3 min wait)

Usage (from repo root):
  python studies/flipflop_drt_integration_pilot/key_figures.py            # print, compare with stored file
  python studies/flipflop_drt_integration_pilot/key_figures.py --write    # (re)write results/key_figures.json
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_demand_v2 import moia_frame  # noqa: E402  (same service-area definition as the demand files)

ROOT_DIR = Path(__file__).resolve().parents[2]
STUDY_DIR = ROOT_DIR / "studies" / "flipflop_drt_integration_pilot"
RESULTS_DIR = STUDY_DIR / "results"
KEY_FIGURES_FILE = RESULTS_DIR / "key_figures.json"

DRAWS_DIR = ROOT_DIR / "data" / "SampleFiles_recovered" / "SampleFiles" / "full_draws"
BASELINE_FILE = DRAWS_DIR / "draws_Baseline.csv"
DRT_FILE = DRAWS_DIR / "draws_DRT_Kostenx1.csv"
MOIA_FILE = ROOT_DIR / "data" / "demand" / "trips_klagenfurt.csv"
ZONES_FILE = ROOT_DIR / "data" / "zones" / "klagenfurt_h1_spitzenzeiten" / "adapted_to_moia_data" / "moia_zone_polygons.geojson"
NETWORK_DIR = ROOT_DIR / "data" / "networks" / "klagenfurt_gip" / "base"
DEMAND_DIR = ROOT_DIR / "data" / "demand" / "flipflop_v2" / "matched" / "klagenfurt_gip"
INIT_DIST_DIR = ROOT_DIR / "data" / "fleetctrl" / "initial_vehicle_distribution" / "klagenfurt_gip"
EVALUATION_FILE = RESULTS_DIR / "v2_evaluation.csv"
SWEEP_FILES = [STUDY_DIR / "scenarios" / n for n in ("scenario_cfg_v2_sweep.csv", "scenario_cfg_v2_sweep_wait6.csv")]

# Assumed level of service (AIT model documentation): DRT access = 30 % of the mean 21 min PT access
PT_ACCESS_MIN = 21.0
DRT_ACCESS_SHARE = 0.3
DETOUR_ASSUMED = 1.4
SERVED_TARGET_PCT = 90.0

DRAW_COLS = ["draw", "trip_id", "drawn_mode", "lat_start", "lon_start", "lat_end", "lon_end"]


# ----------------------------------------------------------------------------------------------
# provenance
# ----------------------------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def input_files():
    """Every file the published figures depend on, relative to the repo root."""
    files = [BASELINE_FILE, DRT_FILE, MOIA_FILE, ZONES_FILE, ROOT_DIR / "data" / "gip_network_ogd.gpkg",
             *sorted(NETWORK_DIR.glob("*")), *sorted(DEMAND_DIR.glob("*.csv")), *sorted(INIT_DIST_DIR.glob("*.csv")),
             STUDY_DIR / "scenarios" / "const_cfg_v2_consistency.yaml", *SWEEP_FILES, EVALUATION_FILE]
    return [f for f in files if f.is_file()]


def provenance():
    return {str(f.relative_to(ROOT_DIR)): sha256(f) for f in input_files()}


# ----------------------------------------------------------------------------------------------
# figures
# ----------------------------------------------------------------------------------------------
def load_mode_choice(moia):
    """All five draws, baseline vs. DRT_Kostenx1, restricted to the service area (MOIA frame), full day.
    Returns (trips_per_draw, in_area merged frame)."""
    base = pd.read_csv(BASELINE_FILE, usecols=DRAW_COLS)
    drt = pd.read_csv(DRT_FILE, usecols=["draw", "trip_id", "drawn_mode"])
    x0, x1, y0, y1 = moia_frame(moia)
    in_frame = (base["lon_start"].between(x0, x1) & base["lat_start"].between(y0, y1)
                & base["lon_end"].between(x0, x1) & base["lat_end"].between(y0, y1))
    merged = base[in_frame].merge(drt, on=["draw", "trip_id"], suffixes=("_base", "_drt"))
    return base.groupby("draw").size(), merged


def switchers_of(merged):
    """Mode switchers: not PT in the baseline, PT (= DRT at PT tariff) in the DRT scenario."""
    return merged[(merged["drawn_mode_base"] != "PT") & (merged["drawn_mode_drt"] == "PT")]


def load_zones():
    import geopandas as gpd
    return gpd.read_file(ZONES_FILE)


def zone_shares(lon, lat, zones):
    """Share of origins per zone (denominator: origins inside the zones) and % of origins outside all zones."""
    import geopandas as gpd
    pts = gpd.GeoDataFrame(geometry=gpd.points_from_xy(lon, lat), crs="EPSG:4326")
    j = gpd.sjoin(pts, zones[["zone_id", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]
    counts = j["zone_id"].value_counts().reindex(zones["zone_id"], fill_value=0)
    return counts / counts.sum(), float(j["zone_id"].isna().mean() * 100)


def mode_choice_figures(moia):
    trips_per_draw, m = load_mode_choice(moia)
    pt_base = (m["drawn_mode_base"] == "PT").groupby(m["draw"]).mean() * 100
    pt_drt = (m["drawn_mode_drt"] == "PT").groupby(m["draw"]).mean() * 100
    switchers = switchers_of(m)
    n_area = m.groupby("draw").size()
    n_sw = switchers.groupby("draw").size()
    figs = {
        "ff_draws": int(trips_per_draw.size),
        "ff_trips_per_draw": int(trips_per_draw.iloc[0]) if trips_per_draw.nunique() == 1 else None,
        "ff_trips_in_area_per_draw": float(n_area.mean()),
        "ff_switchers_unsnapped_per_draw_mean": float(n_sw.mean()),
        "switcher_share_of_trips_pct": float((n_sw / n_area).mean() * 100),
        "pt_share_baseline_pct": float(pt_base.mean()),
        "pt_share_drt_pct": float(pt_drt.mean()),
        "pt_shift_pp": float((pt_drt - pt_base).mean()),
    }
    return figs, switchers


def zone_figures(switchers, moia):
    zones = load_zones()
    moia_sh, moia_out = zone_shares(moia["origin_x"], moia["origin_y"], zones)
    ff_sh, ff_out = zone_shares(switchers["lon_start"], switchers["lat_start"], zones)
    per_draw = [float(zone_shares(g["lon_start"], g["lat_start"], zones)[0].corr(moia_sh)) for _, g in switchers.groupby("draw")]
    centre = int(zones.loc[(ff_sh - moia_sh).abs().values.argmax(), "zone_id"])
    return {
        "zones": int(len(zones)),
        "zone_corr": float(ff_sh.corr(moia_sh)),
        "zone_corr_draw_min": min(per_draw),
        "zone_corr_draw_max": max(per_draw),
        "zone_total_variation": float(0.5 * (ff_sh - moia_sh).abs().sum()),
        "zone_max_divergence_id": centre,
        "zone_max_divergence_ff_pct": float(ff_sh[centre] * 100),
        "zone_max_divergence_moia_pct": float(moia_sh[centre] * 100),
        "ff_origins_outside_zones_pct": ff_out,
        "moia_origins_outside_zones_pct": moia_out,
    }


def moia_volume_figures(moia):
    day = moia["departure_time"] // 86400
    per_day = day.value_counts()
    summary = pd.read_csv(ROOT_DIR / "data" / "demand" / "flipflop_v2" / "demand_summary.csv")
    days = summary[(summary["source"] == "moia") & (summary["day"] != "pooled")]
    ff = summary[summary["source"] == "flipflop"]
    return {
        "moia_trips_total": int(len(moia)),
        "moia_days": int(day.nunique()),
        "moia_trips_per_day_min": int(per_day.min()),
        "moia_trips_per_day_max": int(per_day.max()),
        "moia_requests_per_day_min": int(days["rows_out"].min()),
        "moia_requests_per_day_max": int(days["rows_out"].max()),
        "moia_routable_pct_min": float((days["rows_out"] / days["rows_in"]).min() * 100),
        "moia_routable_pct_max": float((days["rows_out"] / days["rows_in"]).max() * 100),
        "ff_switchers_per_day_mean": float(ff["rows_out"].mean()),
        "ff_switchers_per_day_min": int(ff["rows_out"].min()),
        "ff_switchers_per_day_max": int(ff["rows_out"].max()),
        "volume_ratio_ff_vs_moia_day_min": float(ff["rows_out"].mean() / days["rows_out"].max()),
        "volume_ratio_ff_vs_moia_day_max": float(ff["rows_out"].mean() / days["rows_out"].min()),
    }


def network_figures():
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import dijkstra

    nodes = pd.read_csv(NETWORK_DIR / "nodes.csv")
    edges = pd.read_csv(NETWORK_DIR / "edges.csv")
    n = len(nodes)
    # same sample as build_gip_network.py: 60 x 60 random node pairs, seed 0, beeline > 2 km
    g = coo_matrix((edges["travel_time"].values, (edges["from_node"].values, edges["to_node"].values)), shape=(n, n)).tocsr()
    rng = np.random.default_rng(0)
    src = rng.choice(n, 60, replace=False)
    tt = dijkstra(g, directed=True, indices=src)
    lat0 = nodes["pos_y"].mean()
    xy = np.column_stack([nodes["pos_x"].values * 111_320.0 * np.cos(np.radians(lat0)), nodes["pos_y"].values * 111_320.0])
    dst = rng.choice(n, 60, replace=False)
    bee = np.linalg.norm(xy[src][:, None, :] - xy[dst][None, :, :], axis=2)
    t = tt[:, dst]
    ok = (bee > 2000) & np.isfinite(t)
    return {
        "network_nodes": int(n),
        "network_edges": int(len(edges)),
        "network_speed_kmh": float(edges["distance"].sum() / edges["travel_time"].sum() * 3.6),
        "network_5km_beeline_min": float(np.median(t[ok] / bee[ok]) * 5000 / 60),
    }


def fleet_figures():
    ev = pd.read_csv(EVALUATION_FILE)
    ev["variant"] = ev["variant"].fillna("")
    ev = ev[ev["source"].isin(["moia", "ff"]) & ~ev["scenario"].str.contains("probe")].copy()
    sweep_runs = sum(len(pd.read_csv(f)) for f in SWEEP_FILES)
    std, w6 = ev[ev["variant"] == ""], ev[ev["variant"] == "w6"]
    figs = {"sweep_runs_defined": int(sweep_runs), "sweep_runs_evaluated": int(len(std) + len(w6)),
            "ff_draws_simulated_standard": int(std.loc[std.source == "ff", "set"].nunique()),
            "ff_draws_simulated_w6": int(w6.loc[w6.source == "ff", "set"].nunique()),
            "moia_fleet_min": int(std.loc[std.source == "moia", "fleet"].min()),
            "moia_fleet_max": int(std.loc[std.source == "moia", "fleet"].max()),
            "ff_fleet_min": int(ev.loc[ev.source == "ff", "fleet"].min()),
            "ff_fleet_max": int(ev.loc[ev.source == "ff", "fleet"].max())}

    # implied MOIA fleet (standard config): smallest fleet per calendar day that serves >= 90 %
    moia = std[std.source == "moia"]
    implied = moia[moia.served_pct >= SERVED_TARGET_PCT].groupby("set")["fleet"].min()
    if implied.size != moia["set"].nunique():
        raise ValueError("some MOIA day never reaches the served target in the tested fleet range")
    figs.update({"moia_implied_fleet_min": int(implied.min()), "moia_implied_fleet_max": int(implied.max()),
                 "moia_implied_fleet_median": float(implied.median())})

    # FlipFlop, standard config
    ff = std[std.source == "ff"].groupby("fleet")[["served_pct", "served_within_assumed_los_pct"]].mean()
    reach = ff.index[ff.served_pct >= SERVED_TARGET_PCT]
    figs["ff_std_fleet_for_90"] = int(reach.min()) if len(reach) else None
    for f, row in ff.iterrows():
        figs[f"ff_std_f{f}_served_pct"] = float(row.served_pct)
        figs[f"ff_std_f{f}_within_los_pct"] = float(row.served_within_assumed_los_pct)

    # both sources, assumed-quality config
    for src, g in w6.groupby("source"):
        means = g.groupby("fleet")["served_pct"].mean()
        for f, v in means.items():
            figs[f"{src}_w6_f{f}_served_pct"] = float(v)
        reach, below = means.index[means >= SERVED_TARGET_PCT], means.index[means < SERVED_TARGET_PCT]
        figs[f"{src}_w6_fleet_reaching_90"] = int(reach.min()) if len(reach) else None
        figs[f"{src}_w6_largest_fleet_below_90"] = int(below.max()) if len(below) else None
        figs[f"{src}_w6_fleet_max"] = int(means.index.max())
        figs[f"{src}_w6_draws_or_days"] = int(g["set"].nunique())

    # equal load: requests per vehicle and day, overlapping range of both sources (standard config)
    s = std.assign(load=std["requests"] / std["fleet"])
    m, f_ = s[s.source == "moia"], s[s.source == "ff"]
    lo, hi = max(m.load.min(), f_.load.min()), min(m.load.max(), f_.load.max())
    om, of = m[m.load.between(lo, hi)], f_[f_.load.between(lo, hi)]
    figs.update({
        "equal_load_lo": float(lo), "equal_load_hi": float(hi),
        "equal_load_moia_runs": int(len(om)), "equal_load_ff_runs": int(len(of)),
        "equal_load_moia_served_pct": float(om.served_pct.mean()), "equal_load_ff_served_pct": float(of.served_pct.mean()),
        "equal_load_moia_within_los_pct": float(om.served_within_assumed_los_pct.mean()),
        "equal_load_ff_within_los_pct": float(of.served_within_assumed_los_pct.mean()),
        "equal_load_moia_detour": float(om.detour_median.mean()), "equal_load_ff_detour": float(of.detour_median.mean()),
    })
    return figs


def compute():
    moia = pd.read_csv(MOIA_FILE)
    figs = {"assumed_wait_min": PT_ACCESS_MIN * DRT_ACCESS_SHARE, "assumed_wait_s": round(PT_ACCESS_MIN * DRT_ACCESS_SHARE * 60),
            "assumed_detour": DETOUR_ASSUMED, "pt_access_min": PT_ACCESS_MIN, "drt_access_share_pct": DRT_ACCESS_SHARE * 100}
    mc, switchers = mode_choice_figures(moia)
    figs.update(mc)
    figs.update(zone_figures(switchers, moia))
    figs.update(moia_volume_figures(moia))
    figs.update(network_figures())
    figs.update(fleet_figures())
    return {k: (round(v, 6) if isinstance(v, float) else v) for k, v in figs.items()}


def diff(a: dict, b: dict, tol=1e-6):
    out = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            out.append(f"{k}: {'not computed any more' if k not in a else 'missing in stored file'}")
            continue
        x, y = a[k], b[k]
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and x is not None and y is not None:
            if abs(x - y) > tol * max(1.0, abs(y)):
                out.append(f"{k}: stored {y} != computed {x}")
        elif x != y:
            out.append(f"{k}: stored {y!r} != computed {x!r}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="write results/key_figures.json")
    args = ap.parse_args()
    figs = compute()
    doc = {"figures": figs, "inputs_sha256": provenance()}
    if args.write:
        KEY_FIGURES_FILE.write_text(json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"written {KEY_FIGURES_FILE.relative_to(ROOT_DIR)} ({len(figs)} figures, {len(doc['inputs_sha256'])} input files)")
        return 0
    for k, v in figs.items():
        print(f"{k:40s} {v}")
    if not KEY_FIGURES_FILE.exists():
        print(f"\n{KEY_FIGURES_FILE.name} does not exist yet (use --write)", file=sys.stderr)
        return 1
    stored = json.loads(KEY_FIGURES_FILE.read_text())
    problems = diff(figs, stored["figures"])
    problems += [f"input changed: {k}" for k, h in doc["inputs_sha256"].items() if stored["inputs_sha256"].get(k) != h]
    problems += [f"input missing: {k}" for k in stored["inputs_sha256"] if k not in doc["inputs_sha256"]]
    if problems:
        print("\nkey figures are NOT up to date:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print(f"\nkey figures match {KEY_FIGURES_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
