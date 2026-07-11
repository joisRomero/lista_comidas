"""validate_dotnet_handler — Validate C# endpoint and handler patterns."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

ENDPOINT_MAP_RE = re.compile(r"\bMap(Get|Post|Put|Delete|Patch)\b")
POST_PUT_RE = re.compile(r"\bMap(Post|Put)\b")


def _read_text(path: Path) -> str:
    """Read file content as UTF-8 text."""
    return path.read_text(encoding="utf-8", errors="ignore")


def validate(file_path: str) -> ValidationResult:
    """Validate C# endpoint, handler, and validator file patterns."""
    path = Path(file_path)
    result = ValidationResult(validator="validate_dotnet_handler", target=str(path))
    logger.debug("Validating %s", file_path)

    if path.suffix.lower() != ".cs" or not path.exists():
        return result

    text = _read_text(path)
    name = path.name

    if name.endswith("Endpoint.cs"):
        if "[FromServices]" not in text:
            result.add_warning(
                "EP_FROM_SERVICES",
                "Endpoint should use [FromServices] for dependency injection.",
                suggestion="Inject service dependencies via [FromServices] parameters.",
            )
        if not re.search(r"\bHeaderToken\b", text):
            result.add_warning(
                "EP_HEADER_TOKEN",
                "Endpoint should declare a HeaderToken parameter for auth context.",
                suggestion="Add a HeaderToken parameter to the endpoint signature.",
            )
        if not re.search(r"\.With(?:Summary|Description)\s*\(", text):
            result.add_warning(
                "EP_SWAGGER",
                "Endpoint should include Swagger metadata with WithSummary() or WithDescription().",
            )
        if POST_PUT_RE.search(text) and ".WithValidation<" not in text:
            result.add_warning(
                "EP_VALIDATION",
                "POST/PUT endpoint should use .WithValidation<T>().",
            )

    elif name.endswith("Handler.cs"):
        if "CancellationToken" not in text:
            result.add_warning(
                "HDL_CANCELLATION",
                "Handler should accept a CancellationToken parameter.",
            )
        if re.search(r"\b(Execute|Query)(Async)?\s*\(", text) and "SpResultHelper.ThrowIfError" not in text:
            result.add_error(
                "HDL_SP_HELPER",
                "Handler should call SpResultHelper.ThrowIfError after stored procedure execution.",
                suggestion="Check SP result and call SpResultHelper.ThrowIfError(...).",
            )
        if re.search(r"\b(Query|Execute)(Async)?\s*\(", text) and "CommandDefinition" not in text:
            result.add_warning(
                "HDL_COMMAND_DEF",
                "Handler should use CommandDefinition for Dapper calls.",
            )
        dynamic_match = re.search(r"\bDynamicParameters\b", text)
        if dynamic_match:
            result.add_warning(
                "HDL_NO_DYNAMIC_PARAMS",
                "Avoid DynamicParameters; prefer anonymous objects for parameters.",
                line=text[: dynamic_match.start()].count("\n") + 1,
            )

    elif name.endswith("Validator.cs"):
        if "RuleFor" not in text:
            result.add_error(
                "VAL_NOT_EMPTY",
                "Validator should contain at least one RuleFor expression.",
            )
        if "RuleFor" in text and ".WithErrorCode(\"VAL_" not in text:
            result.add_warning(
                "VAL_ERROR_CODES",
                "Validator should use .WithErrorCode(\"VAL_...\") on rules.",
            )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_dotnet_handler", [".cs"])
