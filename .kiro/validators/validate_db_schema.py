"""validate_db_schema — Validate SQL table schema conventions."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli, line_number

logger = logging.getLogger(__name__)

VALIDATOR_NAME = "validate_db_schema"


def _extract_tables(content: str) -> list:
    """Extract table definitions from SQL content."""
    tables = []
    pattern = re.compile(
        r"\bCREATE\s+TABLE\s+((?:\[[^\]]+\]|\w+))\s*\.\s*((?:\[[^\]]+\]|\w+))\s*\(",
        re.IGNORECASE,
    )
    for match in pattern.finditer(content):
        schema = match.group(1).replace("[", "").replace("]", "")
        table = match.group(2).replace("[", "").replace("]", "")
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
            "schema": schema,
            "table": table,
            "body": content[start + 1:end],
            "line": line_number(content, index=match.start()),
        })
    return tables


def validate(file_path: str) -> ValidationResult:
    path = Path(file_path)
    result = ValidationResult(validator=VALIDATOR_NAME, target=str(path))
    logger.debug("Validating %s", file_path)
    content = path.read_text(encoding="utf-8", errors="ignore")
    tables = _extract_tables(content)

    file_has_extended_props = bool(re.search(r"\bsp_addextendedproperty\b", content, re.IGNORECASE))

    for table_info in tables:
        schema = table_info["schema"]
        table = table_info["table"]
        body = table_info["body"]
        line = table_info["line"]
        if schema.lower() == "log":
            continue

        pk_name = f"PK_{schema}_{table}"
        if not re.search(rf"\bCONSTRAINT\s+\[?{re.escape(pk_name)}\]?\s+PRIMARY\s+KEY\b", body, re.IGNORECASE):
            result.add_error(
                "TBL_PK_NAMING",
                f"{schema}.{table} should name its primary key constraint {pk_name}.",
                line=line,
            )

        has_identity = bool(re.search(r"\bIDENTITY\s*\(", body, re.IGNORECASE))
        has_desc_pk = bool(re.search(r"PRIMARY\s+KEY\s+CLUSTERED\s*\([^\)]*\bDESC\b", body, re.IGNORECASE | re.DOTALL))
        if has_identity and not has_desc_pk:
            result.add_warning(
                "TBL_PK_DESC",
                f"{schema}.{table} identity primary key should use DESC ordering.",
                line=line,
            )

        for fk_match in re.finditer(r"\bCONSTRAINT\s+(\[?[^\]\s]+\]?)\s+FOREIGN\s+KEY\b", body, re.IGNORECASE):
            fk_name = fk_match.group(1).replace("[", "").replace("]", "")
            if not re.match(rf"^FK_{re.escape(schema)}_{re.escape(table)}_.+", fk_name, re.IGNORECASE):
                result.add_warning(
                    "TBL_FK_NAMING",
                    f"Foreign key {fk_name} should follow FK_{schema}_{table}_{{Relation}} naming.",
                    line=line,
                )
                break

        for bool_match in re.finditer(r"^\s*\[?(Is\w+)\]?\s+([^,\n]+)", body, re.IGNORECASE | re.MULTILINE):
            definition = bool_match.group(2).upper().replace(" ", "")
            if "BIT" not in definition or "NOTNULL" not in definition or "DEFAULT((0))" not in definition and "DEFAULT(0)" not in definition and "DEFAULT0" not in definition:
                result.add_warning(
                    "TBL_BOOL_BIT",
                    f"Boolean column {bool_match.group(1)} should be BIT NOT NULL DEFAULT 0.",
                    line=line,
                )
                break

        for date_match in re.finditer(r"^\s*\[?(\w*(?:Date|Timestamp))\]?\s+(DATE|DATETIME(?!OFFSET)|SMALLDATETIME)\b", body, re.IGNORECASE | re.MULTILINE):
            result.add_warning(
                "TBL_DATE_TYPE",
                f"Timestamp-like column {date_match.group(1)} should use DATETIMEOFFSET(7).",
                line=line,
            )
            break

        if not re.search(r"\bRecordStatus\b", body, re.IGNORECASE) or not re.search(r"\bCHECK\b.*?\bRecordStatus\b.*?\bIN\s*\(\s*'A'\s*,\s*'I'\s*,\s*'\*'\s*\)", body, re.IGNORECASE | re.DOTALL):
            result.add_error(
                "TBL_RECORD_STATUS",
                f"{schema}.{table} should define RecordStatus with CHECK IN ('A', 'I', '*').",
                line=line,
            )

        missing_audit = [
            column
            for column in (
                "RecordCreationUser",
                "RecordCreationDate",
                "RecordEditUser",
                "RecordEditDate",
                "RecordStatus",
            )
            if not re.search(rf"\b{column}\b", body, re.IGNORECASE)
        ]
        if missing_audit:
            result.add_error(
                "TBL_AUDIT_COLS",
                f"{schema}.{table} is missing audit columns: {', '.join(missing_audit)}.",
                line=line,
            )

        if not file_has_extended_props:
            result.add_warning(
                "TBL_EXTENDED_PROPS",
                 f"{schema}.{table} should include sp_addextendedproperty for table description.",
                 line=line,
             )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, VALIDATOR_NAME, [".sql"])
