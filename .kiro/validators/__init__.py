"""
ANTA Core Library — Convention Validators (v1.5.5)

Deterministic validation of ANTA conventions. Each validator:
- Receives a file path (or directory)
- Parses content with regex (stdlib only, no external deps)
- Returns ValidationResult with pass/fail/errors/warnings

Usage:
    python config/validators/validate_sp.py path/to/file.sql
    python config/validators/runner.py --all path/to/project/
    python config/validators/runner.py --profile conventions-lint path/to/db/
"""

import json
import logging
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    """A single validation finding."""
    rule: str           # e.g., "QUOTENAME_REQUIRED"
    message: str        # Human-readable description
    file: str           # File path
    line: int = 0       # Line number (0 if not applicable)
    severity: str = "error"  # "error" or "warning"
    suggestion: str = ""     # Suggested fix (optional)


@dataclass
class ValidationResult:
    """Result of running a validator on a file or directory."""
    validator: str = ""
    target: str = ""
    passed: bool = True
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)

    def add_error(self, rule: str, message: str, file: str = "",
                  line: int = 0, suggestion: str = ""):
        self.errors.append(ValidationError(
            rule=rule, message=message, file=file or self.target,
            line=line, severity="error", suggestion=suggestion
        ))
        self.passed = False

    def add_warning(self, rule: str, message: str, file: str = "",
                    line: int = 0, suggestion: str = ""):
        self.warnings.append(ValidationError(
            rule=rule, message=message, file=file or self.target,
            line=line, severity="warning", suggestion=suggestion
        ))

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    def print_report(self):
        """Print human-readable report to stdout."""
        status = "PASS" if self.passed else "FAIL"
        print(f"\n[{self.validator}] {self.target} -> {status}")

        if self.errors:
            print(f"  ERRORS ({len(self.errors)}):")
            for e in self.errors:
                loc = f"L{e.line}" if e.line else ""
                print(f"    [{e.rule}] {e.message} {loc}")
                if e.suggestion:
                    print(f"      -> {e.suggestion}")

        if self.warnings:
            print(f"  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                loc = f"L{w.line}" if w.line else ""
                print(f"    [{w.rule}] {w.message} {loc}")
                if w.suggestion:
                    print(f"      -> {w.suggestion}")

        if self.passed and not self.warnings:
            print(f"  All checks passed.")


def line_number(content: str, match=None, index: int = -1) -> int:
    """Return 1-based line number for a position in content."""
    """Return 1-based line number for a position in content."""
    if match is not None:
        index = match.start()
    if index < 0:
        return 0
    return content.count("\n", 0, index) + 1


def run_validator_cli(validate_fn, validator_name: str, file_extensions: list) -> None:
    """Generic CLI wrapper for any validator. Call from __main__ block."""
    """Generic CLI wrapper for any validator. Call from __main__ block."""
    if len(sys.argv) < 2:
        print(f"Usage: python {validator_name}.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"ERROR: {target} does not exist")
        sys.exit(1)

    results = []
    if target.is_file():
        results.append(validate_fn(str(target)))
    elif target.is_dir():
        for ext in file_extensions:
            for f in sorted(target.rglob(f"*{ext}")):
                results.append(validate_fn(str(f)))
    else:
        print(f"ERROR: {target} is not a file or directory")
        sys.exit(1)

    has_errors = False
    for r in results:
        r.print_report()
        if not r.passed:
            has_errors = True

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    total_files = len(results)

    print(f"\n{'=' * 50}")
    print(f"  {total_files} files, {total_errors} errors, {total_warnings} warnings")
    print(f"  {'FAILED' if has_errors else 'ALL GOOD'}")
    print(f"{'=' * 50}")

    sys.exit(1 if has_errors else 0)
