"""validate_dotnet_project — Validate .NET project structure."""

import logging
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

def _project_root(path: Path) -> Path:
    """Get project root directory from file or directory path."""
    if path.is_dir():
        return path
    if path.suffix.lower() == ".csproj":
        return path.parent
    return path.parent


def validate(file_path: str) -> ValidationResult:
    """Validate .NET project structure and required files."""
    root = _project_root(Path(file_path))
    result = ValidationResult(validator="validate_dotnet_project", target=str(root))
    logger.debug("Validating %s", file_path)

    if not root.exists():
        result.add_error("PROJ_PROGRAM", "Target project path does not exist.")
        return result

    if not (root / "Properties" / "launchSettings.json").exists():
        result.add_error("PROJ_LAUNCH", "Project should include Properties/launchSettings.json.")
    if not (root / "appsettings.Local.json").exists():
        result.add_warning("PROJ_APPSETTINGS", "Project should include appsettings.Local.json.")
    if not (root / "nuget.config").exists():
        result.add_warning("PROJ_NUGET_CONFIG", "Project should include nuget.config.")
    if not (root / "Program.cs").exists():
        result.add_error("PROJ_PROGRAM", "Project should include Program.cs.")

    modules_dir = root / "Modules"
    if not modules_dir.exists() or not any(modules_dir.rglob("*Module.cs")):
        result.add_warning("PROJ_MODULE", "Project should contain at least one *Module.cs file under Modules/.")
    if not any(root.rglob("*StoredProcedures.cs")):
        result.add_warning("PROJ_SP_CLASS", "Project should contain at least one *StoredProcedures.cs file.")

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_dotnet_project", [".csproj"])
