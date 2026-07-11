"""validate_openapi — Validate OpenAPI/Swagger specifications."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli, line_number

logger = logging.getLogger(__name__)

VALIDATOR_NAME = "validate_openapi"


def _extract_path_blocks(content: str) -> list:
    """Extract path blocks from OpenAPI YAML content."""
    matches = list(re.finditer(r"^\s{0,2}(/[^:\n]+):\s*$", content, re.MULTILINE))
    blocks = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        blocks.append({"path": match.group(1).strip(), "block": content[start:end], "line": line_number(content, index=match.start())})
    return blocks


def _extract_method_blocks(path_block: str) -> list:
    """Extract HTTP method blocks from path block."""
    matches = list(re.finditer(r"^\s{2}(get|post|put|patch|delete):\s*$", path_block, re.IGNORECASE | re.MULTILINE))
    methods = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(path_block)
        methods.append({"method": match.group(1).lower(), "block": path_block[start:end]})
    return methods


def _validate_yaml(content: str, result: ValidationResult) -> None:
    """Validate OpenAPI YAML content."""
    path_blocks = _extract_path_blocks(content)
    list_endpoint_missing_pagination = None
    response_issue = None

    for path_info in path_blocks:
        api_path = path_info["path"]
        if not api_path.startswith("/api/v1/"):
            result.add_error(
                "OAS_BASE_PATH",
                f"Path {api_path} should start with /api/v1/.",
                line=path_info["line"],
            )
            break

        for method_info in _extract_method_blocks(path_info["block"]):
            block = method_info["block"]
            method = method_info["method"]
            if method == "get" and "{" not in api_path:
                names = set(re.findall(r"-\s+name:\s*(\w+)", block, re.IGNORECASE))
                if not {"Page", "PageSize"}.issubset(names):
                    list_endpoint_missing_pagination = path_info
            responses_match = re.search(r"\bresponses\s*:\s*(.*?)(?=^\s{2}\w+:|\Z)", block, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            responses_block = responses_match.group(1) if responses_match else ""
            if "200" not in responses_block or ("400" not in responses_block and "500" not in responses_block):
                response_issue = path_info

    if list_endpoint_missing_pagination:
        result.add_warning(
            "OAS_PAGINATION",
            f"List endpoint {list_endpoint_missing_pagination['path']} should declare at least Page and PageSize query params.",
            line=list_endpoint_missing_pagination["line"],
        )

    if not re.search(r"\bsecuritySchemes\b", content, re.IGNORECASE):
        result.add_error(
            "OAS_HEADER_TOKEN",
            "OpenAPI securitySchemes section is missing.",
        )
    else:
        has_code_scheme = bool(re.search(r"^\s{2,6}code\s*:\s*$", content, re.MULTILINE))
        has_header_scheme = bool(re.search(r"^\s{2,6}header\s*:\s*$", content, re.MULTILINE))
        if not has_code_scheme or not has_header_scheme:
            has_legacy = bool(re.search(r"^\s{2,6}HappyAuth\s*:\s*$", content, re.MULTILINE))
            if has_legacy:
                result.add_error(
                    "OAS_HAPPY_LEGACY",
                    "Single 'HappyAuth' scheme is legacy. Use TWO schemes named 'code' and 'header' (matches AddSwaggerWithHappyAuth).",
                )
            elif not has_code_scheme:
                result.add_error(
                    "OAS_HAPPY_CODE",
                    "Missing securityScheme 'code' (apiKey, in: header). Required for Happy auth.",
                )
            elif not has_header_scheme:
                result.add_error(
                    "OAS_HAPPY_HEADER",
                    "Missing securityScheme 'header' (apiKey, in: header). Required for Happy auth.",
                )

    if re.search(r"\bBearerAuth\b|\bbearerAuth\b", content):
        result.add_error(
            "OAS_NO_BEARER",
            "BearerAuth/bearerAuth should not be used in ANTA OpenAPI specs.",
        )

    if not re.search(r"\bErrorItem\b", content) and not re.search(r"\bcode\b.*\bfield\b.*\bmessage\b", content, re.IGNORECASE | re.DOTALL):
        result.add_warning(
            "OAS_ERROR_SCHEMA",
            "Spec should define ErrorItem or an equivalent error schema with code/field/message.",
        )

    if response_issue:
        result.add_warning(
            "OAS_RESPONSES",
            f"Endpoint {response_issue['path']} should declare 200 and at least one error response (400 or 500).",
            line=response_issue["line"],
        )


def _validate_markdown(content: str, result: ValidationResult) -> None:
    """Validate API documentation markdown content."""
    has_delete = bool(re.search(r"\bDELETE\b", content))
    has_item_ops = bool(re.search(r"\b(GET|POST|PUT|PATCH)\b", content))
    has_list_ops = bool(re.search(r"\bGET\b[^\n]*/[^\n/{]+s\b", content))

    if (has_list_ops and "data.items[]" not in content) or (has_item_ops and "data.item{}" not in content) or (has_delete and "data.result{}" not in content):
        result.add_warning(
            "API_RESPONSE_SHAPE",
            "Markdown API-first docs should describe data.items[], data.item{}, and data.result{} response shapes as applicable.",
        )

    if not re.search(r"\b(?:VAL|[A-Z]{2,})_[A-Z0-9_]+\b", content):
        result.add_warning(
            "API_ERROR_CODES",
            "Documentation should include error codes with VAL_ or module-style prefixes.",
        )

    if not re.search(r"stored\s+procedure|\bsp_[A-Za-z0-9_]+\b|SP\s+mapping", content, re.IGNORECASE):
        result.add_warning(
            "API_SP_MAPPING",
            "Documentation should reference the backing stored procedures or include an SP mapping section.",
        )


def validate(file_path: str) -> ValidationResult:
    """Validate OpenAPI YAML or Markdown API documentation."""
    path = Path(file_path)
    result = ValidationResult(validator=VALIDATOR_NAME, target=str(path))
    logger.debug("Validating %s", file_path)
    content = path.read_text(encoding="utf-8", errors="ignore")

    if path.suffix.lower() in {".yaml", ".yml"}:
        _validate_yaml(content, result)
    elif path.suffix.lower() == ".md":
        _validate_markdown(content, result)

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, VALIDATOR_NAME, [".yaml", ".yml", ".md"])
