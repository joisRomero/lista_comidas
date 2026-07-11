"""validate_repo_structure — Validate repository structure."""

import logging
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

def _repo_root(path: Path) -> Path:
    """Get repository root directory."""
    return path if path.is_dir() else path.parent


def validate(file_path: str) -> ValidationResult:
    """Validate repository structure and required files."""
    root = _repo_root(Path(file_path))
    result = ValidationResult(validator="validate_repo_structure", target=str(root))
    logger.debug("Validating %s", file_path)

    if not root.exists():
        result.add_error("REPO_SRC", "Target repository path does not exist.")
        return result

    if not (root / "src").is_dir():
        result.add_error("REPO_SRC", "Repository should include a src/ directory.")
    if not (root / ".gitignore").exists():
        result.add_warning("REPO_GITIGNORE", "Repository should include a .gitignore file.")
    if not ((root / "README.md").exists() or (root / "readme.md").exists()):
        result.add_warning("REPO_README", "Repository should include README.md or readme.md.")

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_repo_structure", [""])
