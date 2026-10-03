# Archive Manifest

## Scope
This manifest records post-cleanup archival placement and provenance (evidence trail).

## Taxonomy
- `archive/runs/*`: execution logs grouped by experiment family.
- `archive/figures/*`: visual outputs grouped by city/experiment family.
- `archive/docs/readme_superseded`: superseded root README variants.
- `archive/data/demand/*`: superseded or dormant demand datasets (inputs no longer used by active study runners).
- `archive/network_setup_scripts/*`: one-time network/zone preparation scripts and notebooks whose output already exists in `data/` and whose own input files are themselves archived; not meant to be re-run.
- `archive/legacy_munich_exploration/*`: first-week Munich exploration (Sept 2025), abandoned when the project moved to Klagenfurt. Distinct from `studies/munich_case_study/`, the upstream FleetPy example, which remains active.
- `archive/legacy_moia_notebooks/*`: May 2026 MOIA exploration notebooks (root `notebooks/` dir), superseded by the properly-homed analysis notebooks in `studies/flipflop_drt_integration_pilot/analysis/`.
- `archive/superseded_scripts/*`: scripts replaced by a working equivalent elsewhere, kept for provenance only.

## Provenance Rules
- Filename prefix (`h1_`, `h2_`, `uc2_`, `uc3_`, `klagenfurt_`) determines experiment-family assignment.
- Ambiguous files are explicitly labeled `unknown`.

## File-Level Mapping
| Archived path | Pre-cleanup path | Inferred experiment | Basis | Confidence |
|---|---|---|---|---|
| `archive/runs/klagenfurt_h1/h1_filtered.log` | root `h1_filtered.log` | klagenfurt_h1_spitzenzeiten | filename prefix | high |
| `archive/runs/klagenfurt_h1/h1_fullday.log` | root `h1_fullday.log` | klagenfurt_h1_spitzenzeiten | filename prefix | high |
| `archive/runs/klagenfurt_h1/h1_rerun.log` | root `h1_rerun.log` | klagenfurt_h1_spitzenzeiten | filename prefix | high |
| `archive/runs/klagenfurt_h2/h2_filtered.log` | root `h2_filtered.log` | klagenfurt_h2_spitzenzeiten | filename prefix | high |
| `archive/runs/klagenfurt_h2/h2_fullday.log` | root `h2_fullday.log` | klagenfurt_h2_spitzenzeiten | filename prefix | high |
| `archive/runs/klagenfurt_h2/h2_rerun.log` | root `h2_rerun.log` | klagenfurt_h2_spitzenzeiten | filename prefix | high |
| `archive/runs/uc2/uc2_filtered.log` | root `uc2_filtered.log` | uc2_age_based | filename prefix | high |
| `archive/runs/uc2/uc2_fullday.log` | root `uc2_fullday.log` | uc2_age_based | filename prefix | high |
| `archive/runs/uc2/uc2_run.log` | root `uc2_run.log` | uc2_age_based | filename prefix | high |
| `archive/runs/uc3/uc3_filtered.log` | root `uc3_filtered.log` | uc3_accessibility | filename prefix | high |
| `archive/runs/uc3/uc3_fullday.log` | root `uc3_fullday.log` | uc3_accessibility | filename prefix | high |
| `archive/runs/klagenfurt_general/klagenfurt_optimized.log` | root `klagenfurt_optimized.log` | klagenfurt_general | filename prefix | medium |
| `archive/runs/klagenfurt_general/klagenfurt_rerun.log` | root `klagenfurt_rerun.log` | klagenfurt_general | filename prefix | medium |
| `archive/runs/klagenfurt_general/klagenfurt_scenario2_optimized.log` | root `klagenfurt_scenario2_optimized.log` | klagenfurt_general | filename prefix | medium |
| `archive/runs/klagenfurt_general/klagenfurt_seed42.log` | root `klagenfurt_seed42.log` | klagenfurt_general | filename prefix | medium |
| `archive/runs/klagenfurt_general/klagenfurt_simulation.log` | root `klagenfurt_simulation.log` | klagenfurt_general | filename prefix | medium |
| `archive/runs/klagenfurt_general/klagenfurt_simulation_optimized.log` | root `klagenfurt_simulation_optimized.log` | klagenfurt_general | filename prefix | medium |
| `archive/runs/regression_checks/standard_bugfix.log` | root `standard_bugfix.log` | cross-study regression | filename semantics | medium |
| `archive/figures/klagenfurt/klagenfurt_filtered_zones_map.png` | root `klagenfurt_filtered_zones_map.png` | klagenfurt zoning | filename prefix | high |
| `archive/figures/klagenfurt/klagenfurt_zones_map_with_basemap.png` | root `klagenfurt_zones_map_with_basemap.png` | klagenfurt zoning | filename prefix | high |
| `archive/figures/klagenfurt/klagenfurt_zones_map.png` | previous `archive/klagenfurt_zones_map.png` | klagenfurt zoning | filename prefix | medium |
| `archive/figures/munich/temporal_test_munich_scenario_1.png` | root `temporal_test_munich_scenario_1.png` | munich scenario test | filename prefix | high |
| `archive/figures/munich/temporal_test_munich_scenario_2.png` | root `temporal_test_munich_scenario_2.png` | munich scenario test | filename prefix | high |
| `archive/docs/readme_superseded/README_old.md` | root `README_old.md` | superseded root docs | filename semantics | high |
| `archive/docs/readme_superseded/README_BACKUP_20251014_183943.md` | root `README_BACKUP_20251014_183943.md` | superseded root docs | filename semantics | high |
| `archive/data/demand/uc1_peaks/` | `data/demand/uc1_peaks/` | dormant demand dataset | no active study const_cfg references | high |
| `archive/data/demand/SoD_demand/` | `data/demand/SoD_demand/` | dormant demand dataset | no active study const_cfg references | high |
| `archive/data/demand/route_193_demand/` | `data/demand/route_193_demand/` | legacy example dataset | referenced only by legacy example outputs | medium |

## 2026-10 Root-Level Cleanup

| Archived path | Pre-cleanup path | Reason | Confidence |
|---|---|---|---|
| `archive/legacy_munich_exploration/munich_analysis.ipynb` | root `munich_analysis.ipynb` | abandoned exploration, not referenced anywhere else | high |
| `archive/legacy_munich_exploration/plot_munich_temporal.py` | root `plot_munich_temporal.py` | same as above | high |
| `archive/legacy_munich_exploration/munich_scenarios_comparison.csv` | root `munich_scenarios_comparison.csv` | same as above | high |
| `archive/legacy_moia_notebooks/moia_additional_tests.ipynb` | root `notebooks/moia_additional_tests.ipynb` | superseded by `studies/flipflop_drt_integration_pilot/analysis/`, not referenced anywhere | high |
| `archive/legacy_moia_notebooks/moia_minimal_variants_results.ipynb` | root `notebooks/moia_minimal_variants_results.ipynb` | same as above | high |
| `archive/legacy_moia_notebooks/moia_vs_baseline_results.ipynb` | root `notebooks/moia_vs_baseline_results.ipynb` | same as above | high |
| `archive/network_setup_scripts/klagenfurt_h1_spitzenzeiten_map_all.py` | root `klagenfurt_h1_spitzenzeiten_map_all.py` | reads already-archived `klagenfurt_network.gpkg`; one-time setup, job done | high |
| `archive/network_setup_scripts/filter_klagenfurt_h1_spitzenzeiten.ipynb` | root `filter_klagenfurt_h1_spitzenzeiten.ipynb` | same as above (produced the now-archived `klagenfurt_network.gpkg`) | high |
| `archive/network_setup_scripts/klagenfurt_h1_spitzenzeiten_zone_mapping.ipynb` | root `klagenfurt_h1_spitzenzeiten_zone_mapping.ipynb` | same as above | high |
| `archive/superseded_scripts/klagenfurt_h1_spitzenzeiten_analysis.py` | root `klagenfurt_h1_spitzenzeiten_analysis.py` | internally broken: three concatenated `main()` definitions (only the last ever executes), which reads nonexistent `users.csv`/`vehicles.csv` and stale scenario-name paths; fully superseded by the working `studies/klagenfurt_h1_spitzenzeiten_case_study/analysis/klagenfurt_h1_spitzenzeiten_analysis.ipynb` | high |

Also moved (not archived, still active — relocated into their case study folders for self-containment, paths fixed and verified working):
- `klagenfurt_h2_spitzenzeiten_analysis.py` → `studies/klagenfurt_h2_spitzenzeiten_case_study/klagenfurt_h2_spitzenzeiten_analysis.py`
- `create_klagenfurt_map_with_basemap.py` → `studies/klagenfurt_h1_spitzenzeiten_case_study/create_klagenfurt_map_with_basemap.py`

Deleted outright (not archived — empty, untracked, no history to preserve): root `scenarios/` directory.

README.md, H1_service_quality.md, and H2_minimum_fleet.md were updated to reference the new/working locations; README.md's duplicated "Installation"/"Simulationen ausführen" sections (one copy with broken escaped-backtick code fences) were also consolidated into one clean version, and stale `studies/uc2_age_based/studies/uc2_study/...` / `studies/uc3_accessibility/studies/uc3_study/...` notebook paths (left over from a pre-cleanup directory structure) were corrected.

## Uncertainty
- Exact simulation run identifiers (timestamp/job-id linkage) are not recoverable from filenames alone. I do not know.
