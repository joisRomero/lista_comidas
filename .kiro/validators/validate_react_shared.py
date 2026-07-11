"""validate_react_shared — Validate React shared components structure."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

REQUIRED = {
    "AntaButton": "error",
    "AntaInput": "error",
    "AntaSelect": "error",
    "AntaForm": "error",
    "AntaTable": "error",
    "AntaModal": "warning",
}


def _shared_root(path: Path) -> Path:
    """Get shared components root directory."""
    if path.is_dir():
        if path.name == "components":
            return path
        if (path / "components").is_dir():
            return path / "components"
        return path
    parts = list(path.parts)
    for index, part in enumerate(parts):
        if part == "components" and index > 0 and parts[index - 1] == "shared":
            return Path(*parts[: index + 1])
    for index, part in enumerate(parts):
        if part == "shared":
            shared_path = Path(*parts[: index + 1])
            if (shared_path / "components").is_dir():
                return shared_path / "components"
            return shared_path
    return path.parent


def _component_files(component_dir: Path) -> list:
    """Get all component files from directory."""
    return list(component_dir.glob("*.tsx")) + list(component_dir.glob("*.ts"))


def validate(file_path: str) -> ValidationResult:
    """Validate React shared components structure."""
    root = _shared_root(Path(file_path))
    result = ValidationResult(validator="validate_react_shared", target=str(root))
    logger.debug("Validating %s", file_path)

    if not root.exists():
        result.add_error("SHARED_BARREL", "Target shared path does not exist.")
        return result

    root_barrel = root / "index.ts"
    barrel_text = root_barrel.read_text(encoding="utf-8", errors="ignore") if root_barrel.exists() else ""

    for name, severity in REQUIRED.items():
        component_dir = root / name
        rule = f"SHARED_{name.upper()}"
        exists = component_dir.is_dir()
        if not exists:
            if severity == "error":
                result.add_error(rule, f"Shared components should include {name}.")
            else:
                result.add_warning(rule, f"Shared components should include {name}.")
            continue

        if name not in barrel_text:
            result.add_error("SHARED_BARREL", f"Root index.ts should re-export {name}.")

        files = _component_files(component_dir)
        if not files:
            continue

        joined = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
        if "forwardRef" not in joined:
            result.add_warning(
                "SHARED_FORWARD_REF",
                f"{name} should use forwardRef for ANTA shared component consistency.",
                file=str(component_dir),
            )
        if not re.search(rf"\b{name}\.displayName\s*=", joined):
            result.add_warning(
                "SHARED_DISPLAY_NAME",
                f"{name} should set .displayName.",
                file=str(component_dir),
            )

    if not root_barrel.exists():
        result.add_error("SHARED_BARREL", "Shared components root should contain index.ts.")

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validate_react_shared.py <shared_directory>")
        sys.exit(1)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"ERROR: {target} does not exist")
        sys.exit(1)
    # Run ONCE on the shared directory — not per-file
    result = validate(str(target))
    result.print_report()
    print(f"\n{'=' * 50}")
    print(f"  1 directory, {len(result.errors)} errors, {len(result.warnings)} warnings")
    print(f"  {'FAILED' if not result.passed else 'ALL GOOD'}")
    print(f"{'=' * 50}")
    sys.exit(0 if result.passed else 1)
