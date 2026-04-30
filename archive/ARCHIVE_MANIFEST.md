# Archive Manifest

## Scope
This manifest records post-cleanup archival placement and provenance (evidence trail).

## Taxonomy
- `archive/runs/*`: execution logs grouped by experiment family.
- `archive/figures/*`: visual outputs grouped by city/experiment family.
- `archive/docs/readme_superseded`: superseded root README variants.
- `archive/data/demand/*`: superseded or dormant demand datasets (inputs no longer used by active study runners).

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

## Uncertainty
- Exact simulation run identifiers (timestamp/job-id linkage) are not recoverable from filenames alone. I do not know.
