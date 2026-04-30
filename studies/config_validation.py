"""
Configuration Validation System for Cross-Hypothesis Comparability

Purpose: Detect config drift across scenarios within each hypothesis.
Prevents silent introduction of environmental changes that confound results.

Usage:
    python config_validation.py [--study STUDY_NAME] [--report PATH]
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


class ConfigValidator:
    """Validates consistency of configs across scenarios within a hypothesis."""

    # Study types: "comparison" (all scenarios same env) vs "intervention" (scenarios test parameter variations)
    STUDY_TYPES = {
        "klagenfurt_h1_spitzenzeiten_case_study": "comparison",
        "klagenfurt_h2_spitzenzeiten_case_study": "comparison",
        "uc2_age_based": "intervention",  # Scenarios test digital competence variants
        "uc3_accessibility": "comparison",
    }

    INVARIANT_FIELDS = {
        # Fields that MUST be identical across all scenarios within a hypothesis
        "network_type",
        "network_name", 
        "demand_name",
        "random_seed",
        "start_time",
        "end_time",
        "time_step",
        "nr_mod_operators",
        "rq_type",
        "op_module",
        "op_rp_batch_optimizer",
        "op_vr_control_func_dict",  # Price function must be identical
        "op_min_wait_time",
        "op_max_wait_time",
        "op_max_detour_time_factor",
        "op_const_boarding_time",
        "op_reoptimisation_timestep",
        "op_zone_system",
    }

    SCENARIO_SPECIFIC_FIELDS = {
        # Fields that SHOULD vary by scenario
        "rq_file",  # demand_requests.csv vs demand_requests_trips.csv
        "scenario_name",
        "user_max_decision_time",  # May vary by scenario
    }

    IGNORE_FIELDS = {
        # Fields that don't affect comparability
        "log_level",
        "route_output_flag",
        "replay_flag",
        "evaluate",
        "keep_old",
        "n_cpu_per_sim",
        "study_name",  # Always fixed per hypothesis
    }

    def __init__(self, studies_dir: Path = None):
        if studies_dir is None:
            studies_dir = Path(__file__).parent
        self.studies_dir = studies_dir
        self.report = {}

    def load_config(self, config_path: Path) -> Dict:
        """Load JSON config, extract scenario_parameters."""
        with open(config_path) as f:
            full_config = json.load(f)
        return full_config.get("scenario_parameters", {})

    def compute_invariant_hash(self, config: Dict) -> str:
        """Compute hash of only invariant fields."""
        invariant_dict = {}
        for field in self.INVARIANT_FIELDS:
            if field in config:
                invariant_dict[field] = config[field]
        
        json_str = json.dumps(invariant_dict, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def validate_study(self, study_name: str) -> Tuple[bool, List[str]]:
        """
        Validate all scenarios within a hypothesis.
        - Comparison studies: All scenarios must have identical invariants
        - Intervention studies: Scenarios intentionally vary parameters (e.g., user_max_decision_time)
        
        Returns: (is_valid, list_of_errors)
        """
        study_path = self.studies_dir / study_name / "results"
        if not study_path.exists():
            return False, [f"Study results dir not found: {study_path}"]

        study_type = self.STUDY_TYPES.get(study_name, "comparison")
        errors = []
        warnings = []
        scenarios = {}

        # Collect all baseline scenarios (non-__trips variants)
        for result_dir in sorted(study_path.iterdir()):
            if not result_dir.is_dir() or result_dir.name.endswith("__trips"):
                continue
            if result_dir.name in ("analysis", "images"):
                continue

            config_file = result_dir / "00_config.json"
            if not config_file.exists():
                errors.append(f"Missing config: {config_file}")
                continue

            config = self.load_config(config_file)
            config_hash = self.compute_invariant_hash(config)
            
            # Filter: Include only scenarios that match expected study naming convention
            # (This filters out old/legacy results from earlier study phases)
            study_prefix = study_name.replace("_case_study", "")
            scenario_name = result_dir.name
            
            # For klagenfurt_h1 studies, filter out "klagenfurt_" prefixed old results
            if "klagenfurt_h" in study_name:
                if scenario_name.startswith("klagenfurt_scenario_"):
                    warnings.append(
                        f"Skipping legacy result: {scenario_name} "
                        f"(network={config.get('network_name')}). "
                        f"Use {study_prefix}_scenario_* naming."
                    )
                    continue
            
            scenarios[result_dir.name] = {
                "config": config,
                "hash": config_hash,
                "path": config_file,
            }

            # Validate __trips variant exists and has matching invariants
            trips_dir = result_dir.parent / (result_dir.name + "__trips")
            if trips_dir.exists():
                trips_config_file = trips_dir / "00_config.json"
                if trips_config_file.exists():
                    trips_config = self.load_config(trips_config_file)
                    trips_hash = self.compute_invariant_hash(trips_config)
                    
                    if trips_hash != config_hash:
                        errors.append(
                            f"Invariant mismatch between {result_dir.name} and {trips_dir.name}\n"
                            f"  Baseline hash: {config_hash}\n"
                            f"  Trips hash:    {trips_hash}"
                        )

        # For comparison studies: All scenarios must share identical invariant hashes
        if study_type == "comparison":
            if scenarios:
                hashes = [s["hash"] for s in scenarios.values()]
                if len(set(hashes)) > 1:
                    errors.append(
                        f"Invariant configs differ across scenarios in {study_name}:\n"
                        + "\n".join(
                            f"  {name}: {s['hash'][:8]}..." 
                            for name, s in scenarios.items()
                        )
                    )

        # For intervention studies: Check network environment is consistent (network_name, zone_system)
        elif study_type == "intervention":
            network_names = set()
            zone_systems = set()
            for name, s in scenarios.items():
                config = s["config"]
                network_names.add(config.get("network_name"))
                zone_systems.add(config.get("op_zone_system"))
            
            if len(network_names) > 1:
                errors.append(
                    f"Network environment inconsistent across {study_name} interventions: "
                    + ", ".join(network_names)
                )
            if len(zone_systems) > 1:
                errors.append(
                    f"Zone system inconsistent across {study_name} interventions: "
                    + ", ".join(zone_systems)
                )

        self.report[study_name] = {
            "valid": len(errors) == 0,
            "scenarios": len(scenarios),
            "study_type": study_type,
            "errors": errors,
            "warnings": warnings,
            "hashes": {name: s["hash"][:8] + "..." for name, s in scenarios.items()},
        }

        return len(errors) == 0, errors

    def validate_all(self) -> bool:
        """Validate all hypothesis studies."""
        hypothesis_studies = [
            "klagenfurt_h1_spitzenzeiten_case_study",
            "klagenfurt_h2_spitzenzeiten_case_study",
            "uc2_age_based",
            "uc3_accessibility",
        ]

        all_valid = True
        for study_name in hypothesis_studies:
            valid, errors = self.validate_study(study_name)
            if not valid:
                all_valid = False
                print(f"\n❌ {study_name}: INVALID")
                for error in errors:
                    print(f"   {error}")
            else:
                scenarios = self.report[study_name]["scenarios"]
                print(f"✓ {study_name}: {scenarios} scenarios validated")

        return all_valid

    def print_report(self):
        """Print validation report."""
        print("\n" + "="*80)
        print("CONFIGURATION VALIDATION REPORT")
        print("="*80)
        
        valid_count = sum(1 for r in self.report.values() if r["valid"])
        total_count = len(self.report)

        print(f"\nResult: {valid_count}/{total_count} hypotheses valid\n")

        for study_name, result in self.report.items():
            status = "✓ PASS" if result["valid"] else "✗ FAIL"
            study_type = result["study_type"]
            type_label = "comparison" if study_type == "comparison" else "intervention"
            print(f"{status} | {study_name} ({result['scenarios']} scenarios, {type_label})")
            
            if result.get("warnings"):
                for warning in result["warnings"]:
                    print(f"      ⚠ {warning}")
            
            if result["errors"]:
                for error in result["errors"]:
                    print(f"      → ERROR: {error}")
            else:
                # Show hash for validation audit trail
                if study_type == "comparison":
                    hashes = list(result["hashes"].values())
                    if hashes:
                        print(f"      → All scenarios: config hash {hashes[0]} (verified identical)")
                else:
                    print(f"      → Scenarios vary by design; environment consistent")

        print("\n" + "="*80)
        print("LEGEND:")
        print("  COMPARISON STUDIES:")
        print("    ✓ All scenarios have identical invariant configs")
        print("    ✗ Configs diverge → not directly comparable (confound detected)")
        print("")
        print("  INTERVENTION STUDIES:")
        print("    ✓ Scenarios intentionally vary parameters; environment consistent")
        print("    ✗ Network/demand environment inconsistent (error)")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(
        description="Validate study configurations for cross-hypothesis comparability"
    )
    parser.add_argument(
        "--study",
        type=str,
        help="Validate single study (default: all)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Save report to JSON file",
    )
    args = parser.parse_args()

    validator = ConfigValidator(Path(__file__).parent)

    if args.study:
        valid, errors = validator.validate_study(args.study)
        validator.print_report()
    else:
        all_valid = validator.validate_all()
        validator.print_report()

    if args.report:
        with open(args.report, "w") as f:
            json.dump(validator.report, f, indent=2)
        print(f"\nReport saved to: {args.report}")

    return 0 if (all_valid if not args.study else valid) else 1


if __name__ == "__main__":
    exit(main())
