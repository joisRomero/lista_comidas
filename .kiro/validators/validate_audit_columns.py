"""validate_audit_columns — Validate SQL table audit column definitions."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli, line_number

logger = logging.getLogger(__name__)

VALIDATOR_NAME = "validate_audit_columns"


def _extract_tables(content: str) -> list:
    """Extract table definitions from SQL content."""
    tables = []
    pattern = re.compile(
        r"\bCREATE\s+TABLE\s+((?:\[[^\]]+\]|\w+))\s*\.\s*((?:\[[^\]]+\]|\w+))\s*\(",
        re.IGNORECASE,
    )
    for match in pattern.finditer(content):
        schema = match.group(1).strip("[]")
        table_name = match.group(2).strip("[]")
        start = match.end() - 1
        depth = 0
        end = start
        for index in range(start, len(content)):
            char = content[index]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    end = index
                    break
        tables.append({
            "body": content[start + 1:end],
            "line": line_number(content, index=match.start()),
            "schema": schema,
            "table_name": table_name,
        })
    return tables


def validate(file_path: str) -> ValidationResult:
    path = Path(file_path)
    result = ValidationResult(validator=VALIDATOR_NAME, target=str(path))
    logger.debug("Validating %s", file_path)
    content = path.read_text(encoding="utf-8", errors="ignore")

    # Patterns for append-only tables (history, log, audit) that don't need Edit/Status columns
    APPEND_ONLY_PATTERNS = re.compile(
        r"(?:History|Log|Audit|StatusHistory|LogDB|LogHttp|LogJob|AuditHttp|AuditEndpoint)",
        re.IGNORECASE,
    )

    tables = _extract_tables(content)
    for table_info in tables:
        body = table_info["body"]
        line = table_info["line"]

        # Detect append-only tables by schema (Log) or table name pattern
        table_name = table_info.get("table_name", "")
        schema = table_info.get("schema", "")
        is_append_only = (
            schema.lower() == "log"
            or bool(APPEND_ONLY_PATTERNS.search(table_name))
        )

        # Helper: match column name with optional square brackets [ColName] or ColName
        def col(name):
            return rf"(?:\[?{name}\]?)"

        # Column presence checks (error if column missing entirely)
        if not re.search(col("RecordCreationUser") + r"\s+VARCHAR\s*\(\s*50\s*\)\s+NOT\s+NULL", body, re.IGNORECASE):
            result.add_error("AUDIT_CREATION_USER", "Missing `RecordCreationUser VARCHAR(50) NOT NULL`.", line=line)

        # Accept DATETIMEOFFSET with or without (7) — DATETIMEOFFSET defaults to (7)
        if not re.search(col("RecordCreationDate") + r"\s+DATETIMEOFFSET", body, re.IGNORECASE):
            result.add_error("AUDIT_CREATION_DATE", "Missing `RecordCreationDate DATETIMEOFFSET`.", line=line)
        elif not re.search(col("RecordCreationDate") + r"\s+DATETIMEOFFSET[^,\n]*DEFAULT\s+SYSDATETIMEOFFSET\s*\(\s*\)", body, re.IGNORECASE):
            result.add_warning("AUDIT_CREATION_DATE_DEFAULT", "RecordCreationDate exists but missing `DEFAULT SYSDATETIMEOFFSET()` (may be set elsewhere).", line=line)

        # Edit/Status columns — error for transactional tables, skip for append-only (History, Log)
        if not re.search(col("RecordEditUser") + r"\s+VARCHAR\s*\(\s*50\s*\)\s+NULL", body, re.IGNORECASE):
            if is_append_only:
                pass  # append-only tables don't need RecordEditUser
            else:
                result.add_error("AUDIT_EDIT_USER", "Missing `RecordEditUser VARCHAR(50) NULL`.", line=line)

        if not re.search(col("RecordEditDate") + r"\s+DATETIMEOFFSET", body, re.IGNORECASE):
            if is_append_only:
                pass  # append-only tables don't need RecordEditDate
            else:
                result.add_error("AUDIT_EDIT_DATE", "Missing `RecordEditDate DATETIMEOFFSET`.", line=line)

        # RecordStatus — error for transactional, skip for append-only
        if not re.search(col("RecordStatus") + r"\s+CHAR\s*\(\s*1\s*\)\s+NOT\s+NULL", body, re.IGNORECASE):
            if is_append_only:
                pass  # append-only tables don't need RecordStatus
            else:
                result.add_error("AUDIT_RECORD_STATUS", "Missing `RecordStatus CHAR(1) NOT NULL`.", line=line)
        elif not re.search(col("RecordStatus") + r"\s+CHAR\s*\(\s*1\s*\)\s+NOT\s+NULL[^,\n]*DEFAULT\s+'A'", body, re.IGNORECASE):
            result.add_warning("AUDIT_RECORD_STATUS_DEFAULT", "RecordStatus exists but missing `DEFAULT 'A'` (may be set elsewhere).", line=line)

        # CHECK constraint — search in FULL file content (may be in ALTER TABLE, not inline)
        # Only warn if not found anywhere in the file for this table
        table_name_match = re.search(r"\bCREATE\s+TABLE\s+((?:\[[^\]]+\]|\w+)\s*\.\s*(?:\[[^\]]+\]|\w+))", content[table_info.get("_start", 0):] if "_start" in table_info else content, re.IGNORECASE)
        has_check = re.search(r"\bCHECK\b[^)]*\bRecordStatus\b[^)]*\bIN\s*\(\s*'A'\s*,\s*'I'\s*,\s*'\*'\s*\)", content, re.IGNORECASE)
        if not has_check:
            result.add_warning("AUDIT_STATUS_CHECK", "No RecordStatus CHECK constraint found in file (expected `CHECK (RecordStatus IN ('A', 'I', '*'))`).", line=line)

    insert_match = re.search(r"\bINSERT\s+INTO\b", content, re.IGNORECASE)
    if insert_match:
        missing_creation_user = False
        for match in re.finditer(r"\bINSERT\s+INTO\s+[^\(\n]+\((.*?)\)\s*(?:VALUES|SELECT)", content, re.IGNORECASE | re.DOTALL):
            if "RECORDCREATIONUSER" not in match.group(1).upper().replace(" ", ""):
                missing_creation_user = True
                break
        if missing_creation_user:
            result.add_warning(
                "AUDIT_INSERT_USER",
                "INSERT statements should include RecordCreationUser.",
                line=line_number(content, index=insert_match.start()),
            )

    update_match = re.search(r"\bUPDATE\b", content, re.IGNORECASE)
    if update_match:
        missing_edit_fields = False
        for match in re.finditer(r"\bUPDATE\b.*?\bSET\b(.*?)(?:\bWHERE\b|;)", content, re.IGNORECASE | re.DOTALL):
            set_block = match.group(1).upper()
            if "RECORDEDITUSER" not in set_block or "RECORDEDITDATE" not in set_block:
                missing_edit_fields = True
                break
        if missing_edit_fields:
            result.add_warning(
                "AUDIT_UPDATE_USER",
                "UPDATE statements should set RecordEditUser and RecordEditDate.",
                line=line_number(content, index=update_match.start()),
            )

    delete_match = re.search(r"\bDELETE\s+FROM\b", content, re.IGNORECASE)
    if delete_match and not re.search(r"\bSET\s+RecordStatus\s*=\s*'\*'", content, re.IGNORECASE):
        result.add_warning(
            "AUDIT_DELETE_SOFT",
            "Prefer soft delete via `SET RecordStatus = '*'` instead of physical DELETE.",
            line=line_number(content, index=delete_match.start()),
        )

    select_match = re.search(r"\bSELECT\b", content, re.IGNORECASE)
    if select_match and not re.search(r"\bRecordStatus\b\s*=\s*'A'|\bRecordStatus\b\s*<>\s*'\*'|\bRecordStatus\b\s*!=\s*'\*'", content, re.IGNORECASE):
        result.add_warning(
            "AUDIT_WHERE_STATUS",
            "SELECT queries should filter active/non-deleted rows using RecordStatus.",
            line=line_number(content, index=select_match.start()),
        )

    if re.search(r"\bGETDATE\s*\(|\bSYSDATETIME\s*\(", content, re.IGNORECASE):
        first = re.search(r"\bGETDATE\s*\(|\bSYSDATETIME\s*\(", content, re.IGNORECASE)
        result.add_warning(
            "AUDIT_NO_GETDATE",
            "Use SYSDATETIMEOFFSET() instead of GETDATE() or SYSDATETIME().",
            line=line_number(content, index=first.start()) if first else 0,
        )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, VALIDATOR_NAME, [".sql"])
