"""validate_dotnet_deps — Validate .NET project dependencies."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

PACKAGE_RE = re.compile(r'<PackageReference\s+Include="([^"]+)"[^>]*Version="([^"]+)"', re.IGNORECASE)
ANTA_PACKAGES = [
    "ANTA.Shared.Common",
    "ANTA.Shared.Common.Data",
    "ANTA.Shared.Common.Api",
    "ANTA.Shared.Common.Validation",
    "ANTA.Shared.Common.Logging",
    "ANTA.Shared.Common.Inspection",
]
RULES = {
    "ANTA.Shared.Common": "DEPS_ANTA_COMMON",
    "ANTA.Shared.Common.Data": "DEPS_ANTA_DATA",
    "ANTA.Shared.Common.Api": "DEPS_ANTA_API",
    "ANTA.Shared.Common.Validation": "DEPS_ANTA_VALIDATION",
    "ANTA.Shared.Common.Logging": "DEPS_ANTA_LOGGING",
    "ANTA.Shared.Common.Inspection": "DEPS_ANTA_INSPECTION",
}


def validate(file_path: str) -> ValidationResult:
    """Validate .csproj file for required ANTA dependencies."""
    path = Path(file_path)
    result = ValidationResult(validator="validate_dotnet_deps", target=str(path))
    logger.debug("Validating %s", file_path)

    if not path.exists() or path.suffix.lower() != ".csproj":
        return result

    text = path.read_text(encoding="utf-8", errors="ignore")
    refs = dict(PACKAGE_RE.findall(text))

    for package in ANTA_PACKAGES:
        if package not in refs:
            result.add_warning(RULES[package], f"Project should reference {package}.")

    # Only check version consistency within ANTA.Shared.Common.* core family.
    # Independent packages have their own release cadence and MUST NOT be
    # compared against the core family.  Add new independents here as needed.
    INDEPENDENT_PACKAGES = {
        "ANTA.Shared.Common.Mapping",
        "ANTA.Shared.Common.Happy",
        "ANTA.Shared.Common.Universal",
        "ANTA.Shared.Common.Arroba",
    }
    common_versions = {}
    for package, version in refs.items():
        if package.startswith("ANTA.Shared.Common") and package not in INDEPENDENT_PACKAGES:
            common_versions.setdefault(version, []).append(package)
    if len(common_versions) > 1:
        detail = "; ".join(f"{v}: {', '.join(pkgs)}" for v, pkgs in common_versions.items())
        result.add_error(
            "DEPS_VERSION_MATCH",
            f"ANTA.Shared.Common.* core packages should use the same version. Found: {detail}",
            suggestion="Align ANTA.Shared.Common core package versions in the .csproj file. Independent packages (Mapping, Happy, Universal, Arroba) are excluded.",
        )

    if re.search(r'Include="AutoMapper"', text, re.IGNORECASE):
        result.add_warning(
            "DEPS_NO_AUTOMAPPER",
            "AutoMapper should not be referenced; use ANTA.Shared.Common.Mapping instead.",
        )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_dotnet_deps", [".csproj"])
