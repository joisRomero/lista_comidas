"""validate_sp — Validate SQL stored procedure conventions."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli, line_number

logger = logging.getLogger(__name__)

VALIDATOR_NAME = "validate_sp"


def _get_proc_header(content: str) -> str:
    """Extract stored procedure header/signature."""
    match = re.search(r"\bCREATE\s+(?:OR\s+ALTER\s+)?PROC(?:EDURE)?\b(.*?)(?:\bAS\b)", content, re.IGNORECASE | re.DOTALL)
    return match.group(1) if match else ""


def _get_proc_name(content: str) -> str:
    """Extract stored procedure name."""
    match = re.search(
        r"\bCREATE\s+(?:OR\s+ALTER\s+)?PROC(?:EDURE)?\s+((?:\[[^\]]+\]|\w+)(?:\s*\.\s*(?:\[[^\]]+\]|\w+))?)",
        content,
        re.IGNORECASE,
    )
    if not match:
        return ""
    return match.group(1).replace("[", "").replace("]", "").strip()


def validate(file_path: str) -> ValidationResult:
    """Validate SQL stored procedure conventions."""
    path = Path(file_path)
    result = ValidationResult(validator=VALIDATOR_NAME, target=str(path))
    logger.debug("Validating %s", file_path)
    content = path.read_text(encoding="utf-8", errors="ignore")

    if not re.search(r"\bSET\s+NOCOUNT\s+ON\b", content, re.IGNORECASE):
        result.add_error(
            "SP_SET_NOCOUNT",
            "Stored procedure should include SET NOCOUNT ON.",
            suggestion="Add `SET NOCOUNT ON;` near the start of the procedure body.",
        )

    if not re.search(r"\bBEGIN\s+TRY\b", content, re.IGNORECASE) or not re.search(r"\bBEGIN\s+CATCH\b", content, re.IGNORECASE):
        result.add_error(
            "SP_TRY_CATCH",
            "Stored procedure should include BEGIN TRY / BEGIN CATCH error handling.",
        )

    catch_match = re.search(r"\bBEGIN\s+CATCH\b(?P<body>.*?)\bEND\s+CATCH\b", content, re.IGNORECASE | re.DOTALL)
    if not catch_match or not re.search(r"\b(?:EXEC(?:UTE)?\s+)?Log\.GetErrorInfo\b", catch_match.group("body"), re.IGNORECASE):
        result.add_error(
            "SP_LOG_ERROR",
            "CATCH block should call Log.GetErrorInfo.",
            line=line_number(content, catch_match) if catch_match else 0,
        )

    join_matches = list(re.finditer(r"\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b", content, re.IGNORECASE))
    missing_nolock = []
    for match in join_matches:
        segment = content[match.start():match.start() + 220]
        if "WITH(NOLOCK)" not in segment.upper().replace(" ", ""):
            missing_nolock.append(match)
    if missing_nolock:
        result.add_warning(
            "SP_NOLOCK",
            "At least one JOIN does not appear to use WITH(NOLOCK).",
            line=line_number(content, missing_nolock[0]),
        )

    if not re.search(r"CHANGE\s+HISTORY", content, re.IGNORECASE):
        result.add_error(
            "SP_CHANGE_HISTORY",
            "Procedure header should include a CHANGE HISTORY section.",
        )

    proc_header = _get_proc_header(content)
    for match in re.finditer(r"(@\w+)\s+[\w\(\),\s]+?(?:\bOUTPUT\b|\bOUT\b)?(?=\s*(?:,|\bAS\b))", proc_header, re.IGNORECASE):
        param_name = match.group(1)
        is_output = bool(re.search(r"\b(?:OUTPUT|OUT)\b", match.group(0), re.IGNORECASE))
        expected_prefix = "@ParamO" if is_output else "@ParamI"
        if not param_name.startswith(expected_prefix):
            result.add_warning(
                "SP_PARAM_PREFIX",
                f"Parameter {param_name} should use prefix {expected_prefix}.",
                line=line_number(content, index=content.find(param_name)),
            )
            break

    declare_match = re.search(r"\bDECLARE\s+(@\w+)", content, re.IGNORECASE)
    if declare_match and not declare_match.group(1).startswith(("@V", "@C")):
        result.add_warning(
            "SP_PARAM_PREFIX",
            f"Declared symbol {declare_match.group(1)} should use @V or @C prefix.",
            line=line_number(content, declare_match),
        )

    if not re.search(r"^\s*--\s*PASO\b", content, re.IGNORECASE | re.MULTILINE):
        result.add_warning(
            "SP_PASO_SECTIONS",
            "Procedure should include at least one `-- PASO` section separator.",
        )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    has_error_select = bool(
        catch_match
        and re.search(
            r"SELECT\b.*?\bAS\s+ErrorCode\b.*?\bAS\s+Field\b.*?\bAS\s+Message\b.*?;\s*RETURN\s*;",
            catch_match.group("body"),
            re.IGNORECASE | re.DOTALL,
        )
    )
    if re.search(r"\bRAISERROR\b", content, re.IGNORECASE) or not has_error_select:
        result.add_warning(
            "SP_ERROR_RETURN",
            "Prefer SELECT ErrorCode/Field/Message + RETURN in error handling instead of RAISERROR or incomplete return shape.",
            line=line_number(content, catch_match) if catch_match else 0,
        )

    if not re.search(r"\bsp_addextendedproperty\b", content, re.IGNORECASE):
        result.add_warning(
            "SP_EXTENDED_PROPS",
            "Procedure should include sp_addextendedproperty metadata.",
        )

    proc_name = _get_proc_name(content).lower()
    if "create" in proc_name and not re.search(r"@ParamIRecordCreationUser\b", proc_header, re.IGNORECASE):
        result.add_warning(
            "SP_AUDIT_PARAMS",
            "Create procedures should declare @ParamIRecordCreationUser.",
        )
    if any(token in proc_name for token in ("update", "delete", "remove")) and not re.search(r"@ParamIRecordEditUser\b", proc_header, re.IGNORECASE):
        result.add_warning(
            "SP_AUDIT_PARAMS",
            "Update/Delete procedures should declare @ParamIRecordEditUser.",
        )

    return result


if __name__ == "__main__":
    run_validator_cli(validate, VALIDATOR_NAME, [".sql"])
