"""validate_react_feature — Validate React feature directory structure."""

import logging
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

def _find_features(path: Path) -> list:
    """Find feature directories to validate."""
    """Given a path, return the list of feature directories to validate.
    - If path IS a features/ parent dir → return direct children
    - If path is a specific feature dir → return [path]
    - If path is a project root → look for features/ recursively and return its children
    """
    if path.name == "features":
        return sorted([d for d in path.iterdir() if d.is_dir()])
    # Check if this looks like a feature dir (has index.ts or *Page.tsx)
    if (path / "index.ts").exists() or any(path.glob("*Page.tsx")):
        return [path]
    # Try to find features/ inside
    for features_dir in path.rglob("features"):
        if features_dir.is_dir():
            return sorted([d for d in features_dir.iterdir() if d.is_dir()])
    return [path]


def find_targets(path: Path) -> list:
    """Resolve directory into individual feature targets."""
    """Runner.py protocol: resolve a directory into individual targets."""
    return _find_features(path)


def validate(file_path: str) -> ValidationResult:
    """Validate React feature directory structure."""
    """Validate a SINGLE feature directory (not its subdirs)."""
    root = Path(file_path)
    if root.is_file():
        root = root.parent
    result = ValidationResult(validator="validate_react_feature", target=str(root))
    logger.debug("Validating %s", file_path)

    if not root.exists():
        result.add_error("FEAT_INDEX", "Target feature path does not exist.")
        return result

    # Page check — only look in THIS dir and direct component subdirs, not recursive
    has_page = any(root.glob("*Page.tsx"))
    if not has_page:
        result.add_warning("FEAT_PAGE", "Feature should contain at least one *Page.tsx file.")
    if not (root / "index.ts").exists():
        result.add_error("FEAT_INDEX", "Feature should expose an index.ts barrel file.")

    has_types_dir = (root / "types").is_dir()
    has_types_file = any(root.glob("*.types.ts"))
    if not has_types_dir and not has_types_file:
        result.add_warning("FEAT_TYPES", "Feature should define shared types via types/ or *.types.ts.")

    # Check hooks — only in THIS dir's children, not recursive
    has_hooks_dir = (root / "hooks").is_dir()
    logic_files = list(root.glob("*.ts")) + list(root.glob("*.tsx"))
    if has_hooks_dir:
        logic_files += list((root / "hooks").glob("*.ts"))
    has_logic = any(
        "use" in p.stem
        or "service" in p.stem.lower()
        or "store" in p.stem.lower()
        for p in logic_files
        if p.name != "index.ts"
    )
    if has_logic and not has_hooks_dir:
        result.add_warning("FEAT_HOOKS", "Feature with logic should expose a hooks/ directory.")

    # Check component subdirs for barrel files
    for child in root.iterdir():
        if child.is_dir() and child.name not in {"hooks", "types", "__tests__", "assets"}:
            has_tsx = any(child.glob("*.tsx"))
            if has_tsx and not (child / "index.ts").exists():
                result.add_warning(
                    "FEAT_COMPONENTS",
                    f"Component folder '{child.name}' should contain its own index.ts barrel file.",
                    file=str(child),
                )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validate_react_feature.py <features_directory|feature_directory>")
        sys.exit(1)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"ERROR: {target} does not exist")
        sys.exit(1)
    # If target is a features/ parent dir, validate each DIRECT child as a feature
    # If target is a specific feature dir, validate just that one
    results = []
    if target.name == "features" or any((child / "index.ts").exists() or any(child.glob("*Page.tsx")) for child in target.iterdir() if child.is_dir()):
        for child in sorted(target.iterdir()):
            if child.is_dir():
                results.append(validate(str(child)))
    else:
        results.append(validate(str(target)))

    has_errors = False
    for r in results:
        r.print_report()
        if not r.passed:
            has_errors = True
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    print(f"\n{'=' * 50}")
    print(f"  {len(results)} features, {total_errors} errors, {total_warnings} warnings")
    print(f"  {'FAILED' if has_errors else 'ALL GOOD'}")
    print(f"{'=' * 50}")
    sys.exit(1 if has_errors else 0)
