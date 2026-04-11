# Experiment Tracks

## Conclusion
Track separation is runner-level (execution-time switch), not file-duplication-level.

## Operating Model
Use existing runners with `--track`:
- `baseline`: uses default `rq_file: demand_requests.csv` from study const config.
- `trips`: auto-generates a temporary scenario CSV by:
  - appending `__trips` to `scenario_name` (output namespace separation),
  - injecting `rq_file=demand_requests_trips.csv` per scenario row.

Temporary CSV artifacts are deleted after execution.

## Commands
- `python run_klagenfurt_h1_spitzenzeiten.py --track baseline`
- `python run_klagenfurt_h1_spitzenzeiten.py --track trips`
- `python run_klagenfurt_h2_spitzenzeiten.py --track baseline`
- `python run_klagenfurt_h2_spitzenzeiten.py --track trips`
- `python run_uc2_age_based.py --track baseline`
- `python run_uc2_age_based.py --track trips`
- `python run_uc3_accessibility.py --track baseline`
- `python run_uc3_accessibility.py --track trips`

## Source-of-Truth Files
- Scenario definitions remain single-source in existing files:
  - `studies/klagenfurt_h1_spitzenzeiten_case_study/scenarios/scenario_cfg_klagenfurt_h1_spitzenzeiten_case_study.csv`
  - `studies/klagenfurt_h2_spitzenzeiten_case_study/scenarios/scenario_cfg_klagenfurt_h2_spitzenzeiten_case_study.csv`
  - `studies/uc2_age_based/scenarios/uc2_scenarios.csv`
  - `studies/uc3_accessibility/scenarios/uc3_scenarios.csv`

## Design Rationale
- Removes duplicated `_trips` runner/config files (structural duplication).
- Preserves baseline scenario definitions unchanged (comparability control).
- Enforces deterministic output isolation through scenario namespace suffixing.
