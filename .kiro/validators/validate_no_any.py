"""validate_no_any — Validate TypeScript files for 'any' type usage."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

TYPE_ONLY_HINT_RE = re.compile(
    r"^\s*import\s+\{\s*([^}]+)\s*\}\s+from\s+['\"][^'\"]+['\"]\s*;?\s*$"
)
TYPE_NAME_RE = re.compile(
    r"^[A-Z][A-Za-z0-9_]*(Type|Types|Props|State|Dto|DTO|Response|Request|Model|Payload|Schema|Input|Output|Result|Params|Query|Filter|Item|Entity|Config|Options|Context|Interface)?$"
)


def _strip_strings_and_comments(text: str) -> list:
    """Remove strings and comments from TypeScript code."""
    lines = []
    in_block_comment = False
    in_single = False
    in_double = False
    in_template = False

    for raw_line in text.splitlines():
        cleaned = []
        i = 0
        while i < len(raw_line):
            pair = raw_line[i : i + 2]

            if in_block_comment:
                if pair == "*/":
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
                continue

            char = raw_line[i]
            if in_single:
                if char == "'" and (i == 0 or raw_line[i - 1] != "\\"):
                    in_single = False
                cleaned.append(" ")
                i += 1
                continue
            if in_double:
                if char == '"' and (i == 0 or raw_line[i - 1] != "\\"):
                    in_double = False
                cleaned.append(" ")
                i += 1
                continue
            if in_template:
                if char == "`" and (i == 0 or raw_line[i - 1] != "\\"):
                    in_template = False
                cleaned.append(" ")
                i += 1
                continue

            if pair == "//":
                break
            if pair == "/*":
                in_block_comment = True
                i += 2
                continue
            if char == "'":
                in_single = True
                cleaned.append(" ")
                i += 1
                continue
            if char == '"':
                in_double = True
                cleaned.append(" ")
                i += 1
                continue
            if char == "`":
                in_template = True
                cleaned.append(" ")
                i += 1
                continue

            cleaned.append(char)
            i += 1

        lines.append("".join(cleaned))

    return lines


def validate(file_path: str) -> ValidationResult:
    """Validate TypeScript file for 'any' type usage."""
    path = Path(file_path)
    result = ValidationResult(validator="validate_no_any", target=str(path))
    logger.debug("Validating %s", file_path)

    if not path.exists() or path.suffix.lower() not in {".ts", ".tsx"}:
        return result

    text = path.read_text(encoding="utf-8", errors="ignore")
    for line_no, line in enumerate(_strip_strings_and_comments(text), start=1):
        if re.search(r":\s*any\b", line):
            result.add_error("TS_NO_ANY", "Avoid ': any' type annotations.", line=line_no)
        if re.search(r"\bas\s+any\b", line):
            result.add_error("TS_NO_AS_ANY", "Avoid 'as any' type assertions.", line=line_no)
        if re.search(r"\bany\s*\[\s*\]", line):
            result.add_error("TS_NO_ANY_ARRAY", "Avoid 'any[]' array types.", line=line_no)

        if line.lstrip().startswith("import type"):
            continue
        match = TYPE_ONLY_HINT_RE.match(line)
        if match:
            names = [item.strip().split(" as ")[0].strip() for item in match.group(1).split(",")]
            if names and all(TYPE_NAME_RE.match(name) for name in names):
                result.add_warning(
                    "TS_IMPORT_TYPE",
                    "Use 'import type' for likely type-only imports.",
                    line=line_no,
                )

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_no_any", [".ts", ".tsx"])
