# FlipFlop DRT Integration Pilot

This study is the first bridge between the recovered FlipFlop mode-choice samples and FleetPy's operational ridepooling simulation.

There are two pilot tracks, sharing the same network, MOIA spatial frame, time window, and fleet scenarios, differing only in which FlipFlop sample they draw from:

- **Neubau pilot**: sourced from the Neubau-specific model (`neubau/draws_Baseline.csv`, ~5,377 trips), which was already scoped to a small area and produced very few MOIA-frame-and-network-covered rows.
- **Klagenfurt pilot**: sourced from the full regional model (`full_draws/draws_Baseline.csv`, 471,140 calibrated trips across all Klagenfurt/Ebenthal), restricted to the same MOIA spatial frame and network coverage. This gives many more retained candidate requests (~22.8k after filtering, before the 100-row pilot cap) since it isn't pre-restricted to Neubau.

## Pilot scope

- Draw: `1` (later draws 2-5 to follow, see Next extensions)
- Time window: 07:00-09:00
- Request limit: first 100 rows ordered by departure time and `trip_id`, after common-frame and network-coverage filtering
- Users: all sampled modes (`Car`, `PT`, `Bike`, and `Foot`)
- Network: `flipflop_neubau_extended` (built from the full extended Klagenfurt network, despite the name — see below)
- Fleet scenarios: 20, 30, and 40 standard vehicles

The all-mode choice is intentional for this first pilot: it measures whether the network and fleet can handle the full sampled trip volume. It must not be interpreted as a behavioral prediction that every traveler requests DRT.

## Run

From the repository root, build the shared pilot network first:

```bash
python studies/flipflop_drt_integration_pilot/build_flipflop_network.py
```

Then prepare demand and run either track:

```bash
# Neubau pilot
python studies/flipflop_drt_integration_pilot/prepare_neubau_baseline_draw1.py
python run_examples.py studies/flipflop_drt_integration_pilot/scenarios/const_cfg_flipflop_drt_integration_pilot.yaml studies/flipflop_drt_integration_pilot/scenarios/scenario_cfg_flipflop_drt_integration_pilot.csv

# Klagenfurt (whole-region) pilot
python studies/flipflop_drt_integration_pilot/prepare_klagenfurt_baseline_draw1.py
python run_examples.py studies/flipflop_drt_integration_pilot/scenarios/const_cfg_flipflop_klagenfurt_pilot.yaml studies/flipflop_drt_integration_pilot/scenarios/scenario_cfg_flipflop_klagenfurt_pilot.csv
```

Each preparation script keeps only trips whose endpoints fall inside the MOIA coordinate frame and are covered by the rebuilt `flipflop_neubau_extended` network (nearest-node distance under 0.005 degrees), maps coordinates to nearest network nodes via a KD-tree, and writes the FleetPy demand file (`flipflop_neubau_pilot` vs. `flipflop_klagenfurt_pilot` demand names, so the two tracks never overwrite each other). The network itself already covers the whole extended Klagenfurt area (43k+ nodes) — it was only named after the Neubau pilot that first used it. The builder also creates a vehicle initialization distribution over the largest connected component. Trips outside the network are rejected rather than silently assigned to distant nodes. The generated demand and simulation results are ignored by Git.

## Spatial comparison

To compare the FlipFlop Neubau points with the existing MOIA trips and FleetPy network nodes on the local street geometry:

```bash
python studies/flipflop_drt_integration_pilot/plot_flipflop_vs_moia_origins_destinations.py
```

This writes `results/flipflop_vs_moia_origins_destinations.png` in this study folder.

The extended street-network version uses the local `klagenfurt_network_extended.gpkg` without replacing the earlier figures:

```bash
python studies/flipflop_drt_integration_pilot/plot_flipflop_vs_moia_with_extended_street_network.py
```

The output is one large map: circles show origins, X markers show destinations; blue is MOIA and orange is FlipFlop.

The original local-street visualization is preserved. To additionally create the OpenStreetMap-backed version, run:

```bash
python studies/flipflop_drt_integration_pilot/plot_flipflop_vs_moia_with_openstreetmap.py
```

This writes `results/flipflop_vs_moia_with_openstreetmap.png` without overwriting the local-street image.

## Interpretation

Compare service rate, waiting time, detours, and utilization across fleet sizes. Before expanding to all five draws or policy scenarios, validate the conversion summary printed by the preparation script, especially the number of requests retained and the nearest-node distance distribution.

## Next extensions

1. Repeat the pilot for Draws 2-5.
2. Add FlipFlop DRT policy scenarios with the same trip IDs and draw numbers.
3. Compare all-mode stress tests with a clearly labelled PT-only or mode-switcher demand definition.