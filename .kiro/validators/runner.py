#!/usr/bin/env python3
"""
runner.py — Orchestrate multiple ANTA validators.

Usage:
    python config/validators/runner.py --all path/to/project/
    python config/validators/runner.py --profile conventions-lint path/to/db/
    python config/validators/runner.py --all --report path/to/project/

Profiles:
    conventions-lint  — BD layer (validate_sp, validate_db_schema, validate_audit_columns)
    spec-gate         — OpenAPI spec (validate_openapi)
    build-unit        — Backend layer (validate_dotnet_handler, validate_dotnet_project, validate_dotnet_deps)
    build-component   — Frontend layer (validate_react_feature, validate_react_shared, validate_no_any)
    structure         — Project structure (validate_repo_structure, validate_docker)
    cross-cutting     — Auth patterns (validate_auth_pattern)
    prototype-gate    — HTML prototypes (validate_html_prototype)
"""

import argparse
import importlib
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Ensure validators directory is in sys.path for imports
_VALIDATORS_DIR = str(Path(__file__).resolve().parent)
if _VALIDATORS_DIR not in sys.path:
    sys.path.insert(0, _VALIDATORS_DIR)

# Profile -> (validator_module, file_extensions)
PROFILES = {
    "conventions-lint": [
        ("validate_sp", [".sql"]),
        ("validate_db_schema", [".sql"]),
        ("validate_audit_columns", [".sql"]),
    ],
    "spec-gate": [
        ("validate_openapi", [".yaml", ".yml"]),
    ],
    "build-unit": [
        ("validate_dotnet_handler", [".cs"]),
        ("validate_dotnet_project", [".csproj"]),
        ("validate_dotnet_deps", [".csproj"]),
    ],
    "build-component": [
        ("validate_react_feature", ["__dir__"]),
        ("validate_react_shared", ["__dir__"]),
        ("validate_no_any", [".ts", ".tsx"]),
    ],
    "structure": [
        ("validate_repo_structure", [""]),
        ("validate_docker", ["Dockerfile", ".yml"]),
    ],
    "cross-cutting": [
        ("validate_auth_pattern", [".cs"]),
    ],
    "prototype-gate": [
        ("validate_html_prototype", ["__dir__"]),
    ],
}


def load_validator(module_name: str) -> tuple:
    """Dynamically import a validator module and return (validate_fn, find_targets_fn).
    find_targets_fn is optional — if present, it resolves a directory into target paths.
    """
    try:
        mod = importlib.import_module(module_name)
        if not hasattr(mod, "validate"):
            print(f"  WARNING: {module_name} has no validate() function, skipping")
            return None, None
        find_targets = getattr(mod, "find_targets", None)
        return mod.validate, find_targets
    except ImportError as e:
        print(f"  WARNING: {module_name} not found ({e}), skipping")
        return None, None


def collect_files(target: Path, extensions: list) -> list:
    """Find files matching extensions in target path."""
    """Find files matching extensions in target path.
    Special extension '__dir__' returns the target directory itself
    (for validators that operate on directories, not individual files).
    """
    if target.is_file():
        return [target]

    if "__dir__" in extensions:
        return [target]

    files = []
    for ext in extensions:
        if ext.startswith("."):
            files.extend(sorted(target.rglob(f"*{ext}")))
        elif ext:
            files.extend(sorted(target.rglob(ext)))
    return files


def run_profile(profile_name: str, target: Path) -> list:
    """Run all validators in a profile against target."""
    logger.info("Running profile %s on %s", profile_name, target)
    if profile_name not in PROFILES:
        print(f"ERROR: Unknown profile '{profile_name}'")
        print(f"Available: {', '.join(PROFILES.keys())}")
        sys.exit(1)

    results = []
    for module_name, extensions in PROFILES[profile_name]:
        validate_fn, find_targets_fn = load_validator(module_name)
        if validate_fn is None:
            continue

        if "__dir__" in extensions and find_targets_fn:
            # Directory-level validator with custom target resolution
            targets = find_targets_fn(target)
            for t in targets:
                results.append(validate_fn(str(t)))
        else:
            files = collect_files(target, extensions)
            for f in files:
                results.append(validate_fn(str(f)))

    return results


def run_all(target: Path) -> list:
    """Run all profiles against target."""
    logger.info("Running all profiles on %s", target)
    results = []
    for profile_name in PROFILES:
        results.extend(run_profile(profile_name, target))
    return results


def main():
    parser = argparse.ArgumentParser(description="ANTA Convention Validator Runner")
    parser.add_argument("target", help="File or directory to validate")
    parser.add_argument("--profile", "-p", help="Validation profile to run")
    parser.add_argument("--all", "-a", action="store_true", help="Run all profiles")
    parser.add_argument("--report", "-r", action="store_true",
                        help="Generate JSON report (validator-report.json)")
    parser.add_argument("--json", action="store_true", help="Output as JSON to stdout")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"ERROR: {target} does not exist")
        sys.exit(1)

    if args.all:
        results = run_all(target)
    elif args.profile:
        results = run_profile(args.profile, target)
    else:
        print("ERROR: Specify --all or --profile <name>")
        parser.print_help()
        sys.exit(1)

    if args.json:
        import dataclasses
        print(json.dumps([dataclasses.asdict(r) for r in results], indent=2))
    else:
        # Print human-readable report
        for r in results:
            r.print_report()

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    total_files = len(results)
    has_errors = any(not r.passed for r in results)

    print(f"\n{'=' * 60}")
    print(f"  ANTA Validator Report")
    print(f"  {total_files} files, {total_errors} errors, {total_warnings} warnings")
    print(f"  {'FAILED' if has_errors else 'ALL GOOD'}")
    print(f"{'=' * 60}")

    # Generate JSON report file if requested
    if args.report:
        import dataclasses
        report_path = target / "validator-report.json" if target.is_dir() else target.parent / "validator-report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump([dataclasses.asdict(r) for r in results], f, indent=2, ensure_ascii=False)
        print(f"\n  Report saved to: {report_path}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
