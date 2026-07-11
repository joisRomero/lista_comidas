"""validate_auth_pattern — Validate C# endpoint authentication patterns."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

ENDPOINT_RE = re.compile(r"\bMap(Get|Post|Put|Delete|Patch)\b")
WRITE_ENDPOINT_RE = re.compile(r"\bMap(Post|Put|Delete|Patch)\b")


def validate(file_path: str) -> ValidationResult:
    """Validate C# file for proper auth pattern usage."""
    path = Path(file_path)
    result = ValidationResult(validator="validate_auth_pattern", target=str(path))
    logger.debug("Validating %s", file_path)

    if not path.exists() or path.suffix.lower() != ".cs":
        return result

    text = path.read_text(encoding="utf-8", errors="ignore")
    if not ENDPOINT_RE.search(text):
        return result

    is_write_endpoint = bool(WRITE_ENDPOINT_RE.search(text))

    if "BearerAuth" in text or re.search(r"\[\s*Authorize\b", text):
        result.add_error(
            "AUTH_NO_BEARER",
            "ANTA auth pattern should not use BearerAuth or [Authorize] in endpoint files.",
            suggestion="Use HeaderToken-based auth context instead.",
        )

    # Write endpoints (POST/PUT/DELETE) MUST have HeaderToken for audit (EmployeeId → SP params).
    # Read endpoints (GET) get auth from middleware — HeaderToken is optional.
    if "HeaderToken" not in text:
        if is_write_endpoint:
            result.add_error(
                "AUTH_HEADER_TOKEN",
                "Write endpoint (POST/PUT/DELETE) must declare HeaderToken for audit context.",
                suggestion="Add [FromServices] HeaderToken headerToken to the endpoint signature.",
            )
        # GET endpoints without HeaderToken are fine — middleware handles auth

    # FromServices and EmployeeId checks only apply to write endpoints.
    # GET endpoints receive auth context from middleware — HeaderToken in their
    # signature is optional and warnings about injection/usage are noise.
    if is_write_endpoint and "HeaderToken" in text:
        if not re.search(r"\[FromServices\][^\n\r]*\bHeaderToken\b", text):
            result.add_warning(
                "AUTH_FROM_SERVICES",
                "HeaderToken should be injected via [FromServices].",
            )
        if not re.search(r"\b(?:headerToken|HeaderToken)\.EmployeeId\b", text):
            result.add_warning(
                "AUTH_EMPLOYEE_ID",
                "Write endpoint should use HeaderToken.EmployeeId for audit context.",
            )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_auth_pattern", [".cs"])
