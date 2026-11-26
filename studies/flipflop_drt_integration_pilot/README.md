# FlipFlop DRT Integration Pilot

This study uses FleetPy's operational ridepooling simulation as an independent check of the FlipFlop (AIT) mode-choice prediction for Klagenfurt, benchmarked against real MOIA trips.

> ## 📌 Start here
>
> **[`analysis/flipflop_consistency_test.ipynb`](analysis/flipflop_consistency_test.ipynb)** is the primary result of this study: the operational consistency test — implied MOIA fleet, fleet needed for the FlipFlop demand at its assumed level of service, and behaviour at equal load. See "Current result" below for how to reproduce it.
>
> **[`analysis/consortium_presentation_flipflop_validation.ipynb`](analysis/consortium_presentation_flipflop_validation.ipynb)** is the short consortium-facing summary; sections 1–2 (spatial, volume) in detail, section 3 summarises the consistency test. It condenses **[`analysis/flipflop_demand_model_validity.ipynb`](analysis/flipflop_demand_model_validity.ipynb)**, which carries the detail for checks 1–2. Everything else in `analysis/` is earlier or supporting work kept for traceability — see the table below and "Earlier work" at the end of this file.

| Notebook | Status |
|---|---|
| `flipflop_consistency_test.ipynb` | **Current — primary result (operational consistency test)** |
| `consortium_presentation_flipflop_validation.ipynb` | Current — consortium summary of all three checks |
| `flipflop_demand_model_validity.ipynb` | Current for checks 1–2 (spatial, volume); its part 3 is superseded by the consistency test |
| `flipflop_drt_demand_construction.ipynb` | Supporting — how the H-A switcher definition was derived (still the basis of `prepare_demand_v2.py`) |
| `flipflop_vs_moia_klagenfurt_bounded_comparison.ipynb` | Supporting — spatial-only comparison, pre-dates the simulated checks |
| `flipflop_drt_feasibility_results.ipynb` | Historical — early H-A results on the previous network build |
| `flipflop_vs_moia_bounded_comparison.ipynb` | Historical — Neubau-track version, kept for reference only |
| ~~`flipflop_vs_moia_simulation_comparison.ipynb`~~ | Moved to [`archive/legacy_flipflop_pilot/`](../../archive/legacy_flipflop_pilot/) — can no longer be re-run |

The report one-pager for the consortium final report is [`FlipFlop_FleetPy_Kurzbericht_2026-11-25.docx`](FlipFlop_FleetPy_Kurzbericht_2026-11-25.docx).

## Current result: operational consistency test

**Question:** does a plausible fleet deliver the level of service FlipFlop *assumed* when predicting the demand?

**Setup** (all scripts in this folder; results under `results/v2_*` and `results/v2w6_*`, aggregated in `results/v2_evaluation.csv`):

| | earlier pipeline (see "Earlier work") | current |
|---|---|---|
| Network | 43k geometry vertices, 30 s floor | `build_gip_network.py`: official GIP link graph (`data/gip_network_ogd.gpkg`), largest strongly connected component only: <!--kf:network_nodes:en0-->15,320<!--/kf--> nodes / <!--kf:network_edges:en0-->33,615<!--/kf--> directed edges, speeds and one-ways per direction from GIP; <!--kf:network_speed_kmh:en1-->34.5<!--/kf--> km/h edge speed, 5 km beeline ≈ <!--kf:network_5km_beeline_min:en0-->9<!--/kf--> min |
| Routing | NetworkBasic (pure Python) | `NetworkBasicWithStoreCpp` (build once: `cd src/routing/cpp_router && python setup.py build_ext --inplace`); a 2,700-request day takes ~2 min instead of hours |
| MOIA demand | 7 calendar days stacked, 06–22 h | `prepare_demand_v2.py`: one file per calendar day (<!--kf:moia_requests_per_day_min:en0-->102<!--/kf-->–<!--kf:moia_requests_per_day_max:en0-->249<!--/kf--> routable requests out of <!--kf:moia_trips_per_day_min:en0-->104<!--/kf-->–<!--kf:moia_trips_per_day_max:en0-->259<!--/kf--> raw trips, <!--kf:moia_routable_pct_min:en0-->90<!--/kf-->–<!--kf:moia_routable_pct_max:en0-->98<!--/kf--> % routable), full day |
| FlipFlop demand | draw 1 | draws 1–5 (<!--kf:ff_switchers_per_day_min:en0~10-->2,550<!--/kf-->–<!--kf:ff_switchers_per_day_max:en0~10-->2,730<!--/kf--> switchers/day each; the per-trip switch is a random realisation of a ~<!--kf:pt_shift_pp:en1-->1.4<!--/kf--> pp shift in the PT share, so single draws are not meaningful) |
| Vehicle start | uniform over network | density of real MOIA origins (`moia_origin_density.csv`) |
| Runner | `run_examples.py` CLI / inline calls | `run_v2.py` (file-based entry point; inline `n_parallel_sim>1` silently loops forever on macOS) |

```bash
python studies/flipflop_drt_integration_pilot/build_gip_network.py
python studies/flipflop_drt_integration_pilot/prepare_demand_v2.py
python studies/flipflop_drt_integration_pilot/run_v2.py scenario_cfg_v2_sweep.csv --parallel 5 --skip-done        # 72 runs, ~20 min
python studies/flipflop_drt_integration_pilot/run_v2.py scenario_cfg_v2_sweep_wait6.csv --parallel 5 --skip-done  # 40 runs, ~7 min
python studies/flipflop_drt_integration_pilot/evaluate_v2.py --pattern 'v2*'
```

**Results** (`analysis/flipflop_consistency_test.ipynb`; assumed level of service = wait ≤ <!--kf:assumed_wait_min:en1-->6.3<!--/kf--> min (AIT: DRT access = <!--kf:drt_access_share_pct:en0-->30<!--/kf--> % of Ø <!--kf:pt_access_min:en0-->21<!--/kf--> min PT access) and in-vehicle time ≤ <!--kf:assumed_detour:en1-->1.4<!--/kf-->× direct — explicit assumptions until AIT supplies absolute values). Two operating configurations are simulated, and the fleet numbers differ between them:

- **standard** (`scenario_cfg_v2_sweep.csv`): usual operating rule, max. 8 min wait
- **assumed quality** (`scenario_cfg_v2_sweep_wait6.csv`, `op_max_wait_time` = <!--kf:assumed_wait_s:en0-->378<!--/kf--> s; all <!--kf:ff_w6_draws_or_days:en0-->5<!--/kf--> FlipFlop draws): the service only accepts requests it can serve within the level of service FlipFlop assumed

1. **Implied MOIA fleet (standard config):** <!--kf:moia_implied_fleet_min:en0-->8<!--/kf-->–<!--kf:moia_implied_fleet_max:en0-->20<!--/kf--> vehicles (median <!--kf:moia_implied_fleet_median:en0-->15<!--/kf--> across the <!--kf:moia_days:en0-->7<!--/kf--> calendar days) serve ≥ 90 % of each day's real trips. This is the calibration question for KMG: if their real fleet is in this range, the simulator is credible for Klagenfurt.
2. **FlipFlop fleet sizing:** in the standard config, <!--kf:ff_std_fleet_for_90:en0-->100<!--/kf--> vehicles serve <!--kf:ff_std_f100_served_pct:en0-->91<!--/kf--> % of the ~<!--kf:ff_switchers_per_day_mean:en0~100-->2,600<!--/kf--> predicted switchers, but only <!--kf:ff_std_f100_within_los_pct:en0-->55<!--/kf--> % within the assumed quality. In the assumed-quality config, 20 / 30 / 40 / 60 / 100 / 150 / 200 vehicles serve **<!--kf:ff_w6_f20_served_pct:en0-->37<!--/kf--> / <!--kf:ff_w6_f30_served_pct:en0-->46<!--/kf--> / <!--kf:ff_w6_f40_served_pct:en0-->56<!--/kf--> / <!--kf:ff_w6_f60_served_pct:en0-->66<!--/kf--> / <!--kf:ff_w6_f100_served_pct:en0-->80<!--/kf--> / <!--kf:ff_w6_f150_served_pct:en0-->90<!--/kf--> / <!--kf:ff_w6_f200_served_pct:en0-->96<!--/kf--> %** of the predicted switchers; real MOIA demand in the same config: 8 / 10 / 15 / 20 vehicles → <!--kf:moia_w6_f8_served_pct:en0-->73<!--/kf--> / <!--kf:moia_w6_f10_served_pct:en0-->79<!--/kf--> / <!--kf:moia_w6_f15_served_pct:en0-->89<!--/kf--> / <!--kf:moia_w6_f20_served_pct:en0-->92<!--/kf--> %. **At equal service quality, ~90 % takes <!--kf:moia_w6_largest_fleet_below_90:en0-->15<!--/kf-->–<!--kf:moia_w6_fleet_reaching_90:en0-->20<!--/kf--> vehicles for real demand and ~<!--kf:ff_w6_fleet_closest_90:en0-->150<!--/kf--> for the predicted demand** (<!--kf:ff_w6_fleet_closest_90:en0-->150<!--/kf--> vehicles: <!--kf:ff_w6_closest_90_served_pct:en0-->90<!--/kf--> %, <!--kf:ff_w6_fleet_max:en0-->200<!--/kf--> vehicles: <!--kf:ff_w6_f200_served_pct:en0-->96<!--/kf--> %). With 20 vehicles, the upper end of what real demand needs, only <!--kf:ff_w6_f20_served_pct:en0-->37<!--/kf--> % of the predicted switchers get the assumed quality.
3. **Same load, same behaviour:** at equal requests per vehicle and day (overlap <!--kf:equal_load_lo:en0-->25<!--/kf-->–<!--kf:equal_load_hi:en0-->62<!--/kf-->), FlipFlop demand is served *better* than real MOIA demand (<!--kf:equal_load_ff_served_pct:en0-->86<!--/kf--> % vs. <!--kf:equal_load_moia_served_pct:en0-->69<!--/kf--> %) because it is spatially denser and pools more (detour <!--kf:equal_load_ff_detour:en2-->1.21<!--/kf--> vs. <!--kf:equal_load_moia_detour:en2-->1.07<!--/kf-->); the share within the assumed quality is practically identical (<!--kf:equal_load_ff_within_los_pct:en0-->49<!--/kf--> % vs. <!--kf:equal_load_moia_within_los_pct:en0-->48<!--/kf--> %). The predicted demand is therefore operationally at least as tractable as real demand — the pooling gap seen with the earlier network build does not persist.

**Bottom line:** the FlipFlop prediction is internally consistent only with a fleet of ~<!--kf:ff_w6_fleet_closest_90:en0-->150<!--/kf--> vehicles for Klagenfurt. With a fleet of the size real demand needs (<!--kf:moia_implied_fleet_min:en0-->8<!--/kf-->–<!--kf:moia_implied_fleet_max:en0-->20<!--/kf--> vehicles, simulated; KMG's actual fleet is not known), about two thirds of the predicted switchers (<!--kf:ff_w6_f20_unserved_pct:en0-->63<!--/kf--> % at 20 vehicles) would not receive the level of service the choice model assumed, and still <!--kf:ff_w6_f40_unserved_pct:en0-->44<!--/kf--> % at 40 vehicles — the prediction is an upper bound and the equilibrium demand is lower.

## Solver: HiGHS instead of Gurobi (branch `highs-solver`, since 2026-11-26)

FleetPy's Alonso-Mora assignment solves a small integer program in every optimisation step. Until 2026-11-21 all results of this study were computed with the commercial solver **Gurobi**. Its license expired on 2026-11-23, and FleetPy does not stop in that case: it retries for 300 s per step and then continues *without* optimising, which would silently produce wrong results. Two changes follow from this:

- **HiGHS** (open source, part of scipy, no license) was added as a third solver option next to Gurobi and CPLEX (`op_solver: HiGHS`, `src/fleetctrl/pooling/batch/AlonsoMora/AlonsoMoraAssignment.py`). It solves the identical model: same variables in the same order, same constraints, same MIP gap and time limit. The study configuration now uses it, so anyone can reproduce the results without a license.
- `run_v2.py` checks before starting that Gurobi works whenever a scenario uses it, and refuses to start otherwise (exit code 3).

**Gurobi vs. HiGHS on <!--kf:solver_cmp_runs:en0-->12<!--/kf--> identical scenarios** (`results/solver_comparison_gurobi_vs_highs.csv`): real MOIA demand gives byte-identical results (<!--kf:solver_cmp_moia_identical:en0-->5<!--/kf--> of <!--kf:solver_cmp_moia_runs:en0-->5<!--/kf--> scenarios, every single assignment the same). For the large FlipFlop days (<!--kf:solver_cmp_ff_runs:en0-->7<!--/kf--> scenarios) the results are not identical: the served share differs by <!--kf:solver_cmp_ff_diff_min_pp:en1-->-0.5<!--/kf--> to +<!--kf:solver_cmp_ff_diff_max_pp:en1-->2.3<!--/kf--> percentage points (mean +<!--kf:solver_cmp_ff_diff_mean_pp:en1-->0.7<!--/kf-->). The likely cause is that many steps have several equally good assignments and the two solvers pick different ones, after which the day evolves differently; this could not be confirmed directly because Gurobi was no longer available. The differences are small against the spread between the five FlipFlop draws and do not change any conclusion, but individual figures moved by about 1–2 points. All <!--kf:sweep_runs_defined:en0-->135<!--/kf--> runs of the sweep were therefore recomputed with HiGHS; mixing solvers would make the runs incomparable. The Gurobi results are kept locally in `results/_gurobi_2026-11-21/` (not in git); branch `main` documents them.

The sweep was also extended: assumed-quality runs now cover all five FlipFlop draws (previously draws 1–3) and fleets of 20, 30 and 200 vehicles (previously 40–150), so the realistic fleet range is simulated directly instead of being inferred.

## Validation: results and their documentation

Every result figure in this README, the root README, the markdown of the three current notebooks and the report one-pager is checked against the simulation, end to end:

| Step | Script | Checked by |
|---|---|---|
| network, demand | `build_gip_network.py`, `prepare_demand_v2.py` | full: rebuilt and byte-compared with `data/` |
| <!--kf:sweep_runs_defined:en0-->135<!--/kf--> simulation runs | `run_v2.py` | full: every run re-simulated, all per-request results must be identical; `results/simulation_manifest.json` records result, input and code hashes; quick: results, inputs and simulation code still match that manifest |
| evaluation | `evaluate_v2.py` → `results/v2_evaluation.csv` | quick: re-evaluation is byte-identical |
| key figures | `key_figures.py` → `results/key_figures.json` (every quoted figure + SHA-256 of all inputs) | quick: re-computed figures and input hashes are identical |
| quoted figures | `check_claims.py` (tags in .md/.ipynb, sentence templates for the .docx) | quick: every quoted figure equals its key figure; deleting tags is caught by a minimum count; each document is rendered like GitHub (pandoc, GFM) and must show no tag fragments and no broken links — without pandoc the step fails |
| notebooks | `analysis/*.ipynb` (use `key_figures.py` functions, so they share one demand definition) | full: re-executed, text outputs identical |
| readability of the whole repo | `check_readability.py`: every tracked .md/.ipynb rendered like GitHub (pandoc, GFM) | quick: no visible raw markup, every relative link and image points to a file tracked in git, notebooks valid without stored errors |
| unit and regression tests | `tests/` (stdlib `unittest`) | quick and full |

```bash
python studies/flipflop_drt_integration_pilot/validate_e2e.py                # quick, ~30 s (pre-commit hook)
python studies/flipflop_drt_integration_pilot/validate_e2e.py --level full   # 1.5-3 h
```

**After an intended change** (new data, code or scenarios): run the sweep → `evaluate_v2.py --pattern 'v2*'` → `key_figures.py --write` → `check_claims.py --update` → re-read every sentence around a changed figure → `validate_e2e.py --level full`. Figures are never typed by hand.

## Checks 1–2: spatial and volume plausibility

Detail in `analysis/flipflop_demand_model_validity.ipynb` (parts 1–2), summarised in the consortium notebook. Demand basis is the same as in the consistency test: switchers from all five draws, full day, service area = MOIA frame.

1. **Spatial validation (zone-level, not bounding-box).** The existing `node_zone_info.csv` zone lookup belongs to a different, 3,435-node network, so it was not reusable by node ID. Instead, both FlipFlop switcher origins and real MOIA origins are joined directly against the real-coordinate zone polygons (`data/zones/klagenfurt_h1_spitzenzeiten/adapted_to_moia_data/moia_zone_polygons.geojson`, <!--kf:zones:en0-->8<!--/kf--> zones built from MOIA's own trip clustering). Result: **correlation <!--kf:zone_corr:en2-->0.87<!--/kf-->** between the two zone-share distributions (<!--kf:zone_corr_draw_min:en2-->0.86<!--/kf-->–<!--kf:zone_corr_draw_max:en2-->0.88<!--/kf--> for the individual draws) — real spatial agreement, not just shared map coverage. The one notable divergence: Zone <!--kf:zone_max_divergence_id:en0-->4<!--/kf--> (city centre) gets <!--kf:zone_max_divergence_ff_pct:en1-->38.6<!--/kf--> % of FlipFlop's predicted switchers vs. <!--kf:zone_max_divergence_moia_pct:en1-->24.3<!--/kf--> % of MOIA's real trips. <!--kf:ff_origins_outside_zones_pct:en0-->12<!--/kf--> % of switcher origins (MOIA: <!--kf:moia_origins_outside_zones_pct:en0-->5<!--/kf--> %) fall outside the zones.
2. **Volume check, with explicit caveats.** `trips_klagenfurt.csv` spans **<!--kf:moia_days:en0-->7<!--/kf--> real calendar days** (<!--kf:moia_trips_per_day_min:en0-->104<!--/kf-->–<!--kf:moia_trips_per_day_max:en0-->259<!--/kf--> trips/day). FlipFlop predicts ~<!--kf:ff_switchers_per_day_mean:en0~100-->2,600<!--/kf--> switchers per day in the same area and operating day (draws 1–5), <!--kf:volume_ratio_ff_vs_moia_day_min:en0-->10<!--/kf-->–<!--kf:volume_ratio_ff_vs_moia_day_max:en0-->26<!--/kf--> times the routable real volume of a single day. This does not prove the model right or wrong: MOIA's volume is *realized* demand under MOIA's own operating constraints (small fleet, limited marketing) — a lower bound on latent demand, not a ceiling. The red flag would be FlipFlop predicting *less* than MOIA already realizes; that is not what happens here.

The zone system with both sources' zone shares is mapped in `results/flipflop_vs_moia_zone_map.png` (written by the consortium presentation notebook):

![FlipFlop vs. MOIA zone shares on the 8 MOIA-derived zones](results/flipflop_vs_moia_zone_map.png)

## Open points

1. **Calibrate the simulator against the real operation:** obtain KMG's fleet size, service hours, wait-time distribution and rejection rate for the data period and check them against the implied fleet (<!--kf:moia_implied_fleet_min:en0-->8<!--/kf-->–<!--kf:moia_implied_fleet_max:en0-->20<!--/kf--> vehicles, standard config).
2. **Replace the assumed level of service with AIT's absolute per-trip values** (access minutes, in-vehicle time in the DRT scenarios); re-run `evaluate_v2.py` with the confirmed thresholds.
3. **Iterate once with AIT:** feed the level of service achieved at a realistic fleet back into the choice model and re-run the sweep on the resulting demand — this yields the equilibrium demand that the consistency test identifies as lower than the prediction.
4. **Price scenarios (H-B):** `prepare_demand_v2.py --price-scenarios DRT_Kostenx0.5 DRT_Kostenx2` and the same sweep, reported as ranges over draws.
5. Investigate the Zone <!--kf:zone_max_divergence_id:en0-->4<!--/kf--> spatial divergence (<!--kf:zone_max_divergence_ff_pct:en1-->38.6<!--/kf--> % vs. <!--kf:zone_max_divergence_moia_pct:en1-->24.3<!--/kf--> % of trip starts) and the <!--kf:ff_origins_outside_zones_pct:en0-->12<!--/kf--> % of switcher origins outside the MOIA-derived zones.

---

## Earlier work (superseded, kept for traceability)

Everything below documents how the study got to the current pipeline. The numbers in this section come from the earlier network build (`flipflop_neubau_extended`, 43k geometry vertices) and partly from a 07:00–09:00 window; **do not cite them as results** — use the sections above.

### Demand tracks

- **Neubau pilot** (`neubau/draws_Baseline.csv`, ~5,377 trips, `prepare_neubau_baseline_draw1.py`): scoped to a small area, produced very few MOIA-frame-and-network-covered rows; abandoned in favour of the whole-region model.
- **Klagenfurt all-mode pilot** (`full_draws/draws_Baseline.csv`, 471,140 calibrated trips, `prepare_klagenfurt_baseline_draw1.py`): ~22.8k candidate requests after filtering, capped at the first 100 in 07:00–09:00; every sampled mode (`Car`, `PT`, `Bike`, `Foot`) treated as a DRT request. A stress test, not a demand forecast.
- **Real MOIA trips** (`data/demand/trips_klagenfurt.csv`, `prepare_moia_klagenfurt_baseline.py`): simulated the same way for comparison; originally 07:00–09:00, later the full 06:00–22:00 day with all 7 calendar days stacked.
- **Hypothesis H-A, realistic mode-switchers** (`prepare_drt_switcher_demand.py`): a trip counts only if it is `PT` under `draws_DRT_Kostenx1.csv` (DRT at PT tariff) but not `PT` in `draws_Baseline.csv`; full day 06:00–22:00. This definition is what `prepare_demand_v2.py` uses today.

The two `*_baseline_draw1.py` scripts carry a deprecation note: they still have the connected-component defect described below, left unfixed so the historical numbers stay reproducible.

### Running the earlier pipeline

```bash
python studies/flipflop_drt_integration_pilot/build_flipflop_network.py

# Klagenfurt all-mode pilot and MOIA comparison (07:00-09:00)
python studies/flipflop_drt_integration_pilot/prepare_klagenfurt_baseline_draw1.py
python run_examples.py studies/flipflop_drt_integration_pilot/scenarios/const_cfg_flipflop_klagenfurt_pilot.yaml studies/flipflop_drt_integration_pilot/scenarios/scenario_cfg_flipflop_klagenfurt_pilot.csv
python studies/flipflop_drt_integration_pilot/prepare_moia_klagenfurt_baseline.py
python run_examples.py studies/flipflop_drt_integration_pilot/scenarios/const_cfg_moia_klagenfurt_pilot.yaml studies/flipflop_drt_integration_pilot/scenarios/scenario_cfg_moia_klagenfurt_pilot.csv

# H-A switchers on the earlier network
python studies/flipflop_drt_integration_pilot/prepare_drt_switcher_demand.py --price-scenario DRT_Kostenx1 --draw 1
python run_examples.py studies/flipflop_drt_integration_pilot/scenarios/const_cfg_flipflop_drt_feasibility.yaml studies/flipflop_drt_integration_pilot/scenarios/scenario_cfg_flipflop_drt_feasibility.csv
```

The Neubau configs (`const_cfg_flipflop_drt_integration_pilot.yaml`, `scenario_cfg_flipflop_drt_integration_pilot.csv`) still exist. All preparation scripts map coordinates to the nearest network node via a KD-tree (rejecting endpoints more than 0.005° away) and write to distinct demand names, so runs never overwrite each other. `python run_examples.py <const_cfg> <scenario_cfg>` requires this repo's CLI fix in `run_examples.py` (`sys.argv[1:]`).

### Spatial comparison maps

These plotting scripts still run and are independent of the simulation pipeline:

```bash
python studies/flipflop_drt_integration_pilot/plot_flipflop_vs_moia_origins_destinations.py              # results/flipflop_vs_moia_origins_destinations.png
python studies/flipflop_drt_integration_pilot/plot_flipflop_vs_moia_with_extended_street_network.py      # on klagenfurt_network_extended.gpkg
python studies/flipflop_drt_integration_pilot/plot_flipflop_vs_moia_with_openstreetmap.py                # results/flipflop_vs_moia_with_openstreetmap.png
```

Circles show origins, X markers destinations; blue is MOIA, orange is FlipFlop.

### All-mode stress test vs. MOIA (07:00–09:00)

Notebook archived at `archive/legacy_flipflop_pilot/flipflop_vs_moia_simulation_comparison.ipynb` (not re-runnable: the `moia_klagenfurt_baseline_30` result directory no longer exists). FlipFlop all-mode n=100 (~91 routable), MOIA n=49:

| Fleet | FlipFlop served | MOIA served |
|---|---|---|
| 20 | 5% | 2% |
| 30 | 10% | 2% |
| 40 | 11% | 4% |

Both sources landed in the same low service-rate range; absolute served counts were 1–11 requests, so the percentages were only indicative.

### H-A on the earlier network (`flipflop_drt_feasibility_results.ipynb`)

2,066 switcher requests (draw 1, MOIA frame, network-connected), full day:

| Fleet | Served | Service rate | Shared rides | Rides/vehicle |
|---|---|---|---|---|
| 20 | 76 | 3.7% | 74% | 3.80 |
| 40 | 148 | 7.2% | 76% | 3.70 |
| 60 | 226 | 10.9% | 75% | 3.77 |

Part 3 of `flipflop_demand_model_validity.ipynb` compared this with MOIA over the same full day (615 requests, all 7 days stacked): service rates 3.1–3.7 % / 7.2–7.3 % / 10.9–12.5 % at 20 / 40 / 60 vehicles, shared rides 74–76 % (H-A) vs. 13–21 % (MOIA). The low service rates were largely a property of that network build; the consistency test on the GIP network replaces this comparison and the pooling gap does not persist there.

### A routing bug found while building the H-A demand

Snapping a trip's endpoints to the nearest network node is not enough on its own: a node can be geometrically close but sit in a small, disconnected fragment of the street graph extracted from `klagenfurt_network_extended.gpkg`, so FleetPy can never route to or from it regardless of fleet size. 6,316 of that network's 43,137 nodes were outside the largest connected component. `prepare_drt_switcher_demand.py` and `prepare_moia_klagenfurt_baseline.py` filter against `data/fleetctrl/initial_vehicle_distribution/flipflop_neubau_extended/largest_component_uniform.csv`; the two `*_baseline_draw1.py` scripts do not. The GIP network of the current pipeline is restricted to its largest strongly connected component at build time, so the issue does not arise there.
