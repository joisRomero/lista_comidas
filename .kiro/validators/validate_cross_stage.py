"""validate_cross_stage — Validate advisory cross-stage consistency."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, line_number, run_validator_cli

logger = logging.getLogger(__name__)

VALIDATOR_NAME = "validate_cross_stage"
ERROR_CODE_PATTERN = re.compile(r"\b(?:VAL|BUS)_[A-Z0-9_]+\b")


def _looks_like_inception_root(path: Path) -> bool:
    """Return True when path looks like an inception artifacts directory."""
    return path.is_dir() and (
        path.name.lower() == "inception"
        or (path / "requirements").exists()
        or (path / "user-stories").exists()
        or (path / "api-contracts").exists()
    )


def _resolve_inception_root(path: Path) -> Path:
    """Resolve inception root from file or directory input."""
    current = path if path.is_dir() else path.parent
    for candidate in (current, *current.parents):
        if _looks_like_inception_root(candidate):
            return candidate
    return current


def _find_artifact(root: Path, preferred_relative_path: str, fallback_patterns: list) -> Path | None:
    """Find artifact by preferred path first, then by recursive filename lookup."""
    preferred = root / preferred_relative_path
    if preferred.is_file():
        return preferred

    for pattern in fallback_patterns:
        matches = sorted(path for path in root.rglob(pattern) if path.is_file())
        if matches:
            return matches[0]

    return None


def _read_text(path: Path | None) -> str:
    """Read text content safely."""
    if path is None or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_error_codes(content: str) -> set[str]:
    """Extract typed error codes, including compact numeric ranges."""
    codes = set(ERROR_CODE_PATTERN.findall(content))

    for match in re.finditer(r"\b((?:VAL|BUS)_[A-Z][A-Z0-9_]*?)(\d{2,4})\s*(?:\.\.|-)\s*(\d{2,4})\b", content):
        prefix = match.group(1)
        start_number = int(match.group(2))
        end_number = int(match.group(3))
        width = len(match.group(2))

        if end_number < start_number or end_number - start_number > 100:
            continue

        for number in range(start_number, end_number + 1):
            codes.add(f"{prefix}{number:0{width}d}")

    return codes


def _extract_functional_requirements(content: str) -> set[str]:
    """Extract FR markers or section 4.x identifiers from requirements."""
    markers = {match.group(0).upper() for match in re.finditer(r"\bFR-[A-Z0-9._-]+\b", content, re.IGNORECASE)}

    for match in re.finditer(r"§\s*(4(?:\.\d+)+)\b", content):
        markers.add(match.group(1))

    for match in re.finditer(r"^\s{0,3}#{1,6}\s+(4(?:\.\d+)+)\b", content, re.MULTILINE):
        markers.add(match.group(1))

    return markers


def _extract_path_blocks(content: str) -> list:
    """Extract OpenAPI path blocks from raw YAML text."""
    matches = list(re.finditer(r"^\s{0,2}(/[^:\n]+):\s*$", content, re.MULTILINE))
    blocks = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        blocks.append({
            "path": match.group(1).strip(),
            "block": content[start:end],
            "line": line_number(content, index=match.start()),
        })
    return blocks


def _extract_method_blocks(path_block: str) -> list:
    """Extract HTTP method blocks from a single OpenAPI path block."""
    matches = list(re.finditer(r"^\s{2,6}(get|post|put|patch|delete):\s*$", path_block, re.IGNORECASE | re.MULTILINE))
    methods = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(path_block)
        methods.append({"method": match.group(1).lower(), "block": path_block[start:end]})
    return methods


def _extract_endpoints(content: str) -> list:
    """Extract endpoint signatures from OpenAPI YAML."""
    endpoints = []
    for path_info in _extract_path_blocks(content):
        for method_info in _extract_method_blocks(path_info["block"]):
            endpoints.append(f"{method_info['method'].upper()} {path_info['path']}")
    return sorted(set(endpoints))


def _extract_hu_markers(content: str) -> set[str]:
    """Extract HU section markers from user stories markdown."""
    markers = set()

    for match in re.finditer(r"^\s*#{2,6}\s+(HU(?:[-\s][A-Z0-9_-]+)?)\b", content, re.IGNORECASE | re.MULTILINE):
        markers.add(match.group(1).upper())

    for match in re.finditer(r"^\s*#{2,6}\s+((?:\d{3}-\d{5}-\d{3})|(?:\d+-\d+-\d+))\b", content, re.MULTILINE):
        markers.add(match.group(1))

    return markers


def _validate_error_code_consistency(
    result: ValidationResult,
    requirements_path: Path | None,
    stories_path: Path | None,
    openapi_path: Path | None,
    api_summary_path: Path | None,
    requirements_content: str,
    stories_content: str,
    openapi_content: str,
    api_summary_content: str,
) -> None:
    """Validate advisory cross-stage error code consistency."""
    requirement_codes = _extract_error_codes(requirements_content)
    story_codes = _extract_error_codes(stories_content)
    openapi_codes = _extract_error_codes(openapi_content)
    api_summary_codes = _extract_error_codes(api_summary_content)

    missing_from_requirements = sorted(story_codes - requirement_codes)
    if missing_from_requirements:
        result.add_warning(
            "CROSS_ERROR_CODES",
            f"stories.md references codes not present in requirements.md: {', '.join(missing_from_requirements)}.",
            file=str(stories_path or result.target),
            suggestion="Back-propagate confirmed downstream codes into requirements business/validation rules.",
        )

    orphan_summary_codes = sorted(api_summary_codes - openapi_codes)
    if orphan_summary_codes:
        result.add_warning(
            "CROSS_ERROR_CODES",
            f"api-summary.md references codes not present in openapi.yaml: {', '.join(orphan_summary_codes)}.",
            file=str(api_summary_path or result.target),
            suggestion="Align api-summary.md with the source OpenAPI spec or document the missing responses there first.",
        )

    documented_codes = requirement_codes | story_codes
    undocumented_openapi_codes = sorted(openapi_codes - documented_codes)
    if undocumented_openapi_codes:
        result.add_warning(
            "CROSS_ERROR_CODES",
            f"openapi.yaml contains codes not documented in requirements.md or stories.md: {', '.join(undocumented_openapi_codes)}.",
            file=str(openapi_path or result.target),
            suggestion="Document API-visible validation/business codes upstream in requirements or user stories.",
        )


def _validate_endpoint_coverage(
    result: ValidationResult,
    requirements_path: Path | None,
    requirements_content: str,
    openapi_content: str,
) -> None:
    """Validate heuristic FR-to-endpoint coverage."""
    requirement_markers = _extract_functional_requirements(requirements_content)
    endpoints = _extract_endpoints(openapi_content)

    if requirement_markers and not endpoints:
        result.add_warning(
            "CROSS_ENDPOINT_COVERAGE",
            f"requirements.md contains {len(requirement_markers)} FR markers/section 4.x entries, but openapi.yaml exposes 0 endpoints.",
            file=str(requirements_path or result.target),
            suggestion="Check whether api-contracts/openapi.yaml is missing or still pending for this inception package.",
        )


def _validate_hu_coverage(
    result: ValidationResult,
    stories_path: Path | None,
    stories_content: str,
    openapi_content: str,
) -> None:
    """Validate heuristic HU-to-endpoint coverage."""
    hu_markers = _extract_hu_markers(stories_content)
    endpoints = _extract_endpoints(openapi_content)

    if hu_markers and not endpoints:
        result.add_warning(
            "CROSS_HU_COVERAGE",
            f"stories.md contains {len(hu_markers)} HU markers, but openapi.yaml exposes 0 endpoints.",
            file=str(stories_path or result.target),
            suggestion="Check whether API Contract Design has not been generated yet or the spec is in a different location.",
        )


def _validate_auth_scheme(result: ValidationResult, openapi_path: Path | None, openapi_content: str) -> None:
    """Validate advisory auth scheme consistency in OpenAPI."""
    if not openapi_content:
        return

    security_schemes_match = re.search(r"\bsecuritySchemes\b", openapi_content, re.IGNORECASE)
    if not security_schemes_match:
        result.add_warning(
            "CROSS_AUTH_SCHEME",
            "openapi.yaml is missing a securitySchemes section; expected Happy auth schemes named 'code' and 'header'.",
            file=str(openapi_path or result.target),
        )
        return

    has_code_scheme = bool(re.search(r"^\s{2,6}code\s*:\s*$", openapi_content, re.MULTILINE))
    has_header_scheme = bool(re.search(r"^\s{2,6}header\s*:\s*$", openapi_content, re.MULTILINE))
    if has_code_scheme and has_header_scheme:
        return

    legacy_match = re.search(r"^\s{2,6}HappyAuth\s*:\s*$", openapi_content, re.MULTILINE)
    if legacy_match:
        result.add_warning(
            "CROSS_AUTH_SCHEME",
            "openapi.yaml uses legacy 'HappyAuth'. Prefer TWO security schemes named 'code' and 'header' for cross-stage consistency.",
            file=str(openapi_path or result.target),
            line=line_number(openapi_content, match=legacy_match),
        )
    elif not has_code_scheme:
        result.add_warning(
            "CROSS_AUTH_SCHEME",
            "openapi.yaml is missing securityScheme 'code' (apiKey, in: header).",
            file=str(openapi_path or result.target),
            line=line_number(openapi_content, match=security_schemes_match),
        )
    elif not has_header_scheme:
        result.add_warning(
            "CROSS_AUTH_SCHEME",
            "openapi.yaml is missing securityScheme 'header' (apiKey, in: header).",
            file=str(openapi_path or result.target),
            line=line_number(openapi_content, match=security_schemes_match),
        )


def validate(directory_path: str) -> ValidationResult:
    """Validate advisory consistency across inception-stage artifacts."""
    root = _resolve_inception_root(Path(directory_path))
    result = ValidationResult(validator=VALIDATOR_NAME, target=str(root))
    logger.debug("Validating %s", directory_path)

    requirements_path = _find_artifact(root, "requirements/requirements.md", ["requirements.md"])
    stories_path = _find_artifact(root, "user-stories/stories.md", ["stories.md"])
    openapi_path = _find_artifact(root, "api-contracts/openapi.yaml", ["openapi.yaml", "openapi.yml"])
    api_summary_path = _find_artifact(root, "api-contracts/api-summary.md", ["api-summary.md"])

    requirements_content = _read_text(requirements_path)
    stories_content = _read_text(stories_path)
    openapi_content = _read_text(openapi_path)
    api_summary_content = _read_text(api_summary_path)

    _validate_error_code_consistency(
        result,
        requirements_path,
        stories_path,
        openapi_path,
        api_summary_path,
        requirements_content,
        stories_content,
        openapi_content,
        api_summary_content,
    )
    _validate_endpoint_coverage(result, requirements_path, requirements_content, openapi_content)
    _validate_hu_coverage(result, stories_path, stories_content, openapi_content)
    _validate_auth_scheme(result, openapi_path, openapi_content)

    logger.debug("Validation complete: %s — %d errors, %d warnings", directory_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, VALIDATOR_NAME, ["requirements.md"])
