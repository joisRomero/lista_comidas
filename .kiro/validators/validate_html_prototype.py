"""validate_html_prototype — Validate CSS classes and variables in prototype HTML files.

Reads anta-prototype.css dynamically to extract defined classes and :root variables,
then verifies every class and variable used in HTML files exists in the CSS.
Also checks structural patterns (card-body wrapping, tab-panel visibility).

Usage:
    python validate_html_prototype.py path/to/aidlc-docs/inception/prototypes/
"""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, ValidationError, run_validator_cli

logger = logging.getLogger(__name__)

# Classes safe to ignore — standard HTML/utility classes not defined in anta-prototype.css
IGNORED_CLASSES = frozenset({
    "hidden", "active", "disabled", "selected",
})

# Known class mistakes: wrong → correct
KNOWN_MISTAKES = {
    "anta-tabs-tab": "anta-tab",
    "anta-form-help": "anta-form-hint",
    "anta-form-error": "anta-form-hint anta-form-hint--error",
}


def _parse_css_classes(css_text: str) -> set:
    """Extract all class names defined in CSS (selectors starting with .)."""
    classes = set()
    for m in re.finditer(r"\.([a-zA-Z][a-zA-Z0-9_-]*)", css_text):
        classes.add(m.group(1))
    return classes


def _parse_css_variables(css_text: str) -> set:
    """Extract all CSS custom property names defined in :root."""
    variables = set()
    root_match = re.search(r":root\s*\{([^}]+)\}", css_text, re.DOTALL)
    if root_match:
        for m in re.finditer(r"--([a-zA-Z][a-zA-Z0-9_-]*)\s*:", root_match.group(1)):
            variables.add(m.group(1))
    return variables


def _extract_html_classes(html_text: str) -> list:
    """Extract (class_name, line_number) tuples from HTML class attributes."""
    findings = []
    for lineno, line in enumerate(html_text.splitlines(), 1):
        for m in re.finditer(r'class="([^"]+)"', line):
            for cls in m.group(1).split():
                findings.append((cls, lineno))
    return findings


def _extract_html_variables(html_text: str) -> list:
    """Extract (variable_name, line_number) tuples from var(--name) references."""
    findings = []
    for lineno, line in enumerate(html_text.splitlines(), 1):
        for m in re.finditer(r"var\(--([a-zA-Z][a-zA-Z0-9_-]*)\)", line):
            findings.append((m.group(1), lineno))
    return findings


def validate(file_path: str) -> ValidationResult:
    """Validate HTML prototype files in a prototypes directory."""
    target = Path(file_path)
    result = ValidationResult(
        validator="validate_html_prototype",
        target=str(target),
    )

    # Resolve directory
    proto_dir = target if target.is_dir() else target.parent
    logger.debug("Validating prototypes in %s", proto_dir)

    # Find CSS file
    css_file = proto_dir / "anta-prototype.css"
    if not css_file.exists():
        # Try parent or skill assets as fallback
        for candidate in [
            proto_dir.parent / "anta-prototype.css",
            Path(__file__).resolve().parent.parent / "skills" / "html-prototype" / "assets" / "anta-prototype.css",
        ]:
            if candidate.exists():
                css_file = candidate
                break

    if not css_file.exists():
        result.add_error(
            "CSS_FILE_MISSING",
            "anta-prototype.css not found in prototypes directory or skill assets.",
        )
        return result

    # Parse CSS
    css_text = css_file.read_text(encoding="utf-8", errors="ignore")
    defined_classes = _parse_css_classes(css_text)
    defined_vars = _parse_css_variables(css_text)
    logger.debug("CSS: %d classes, %d variables defined", len(defined_classes), len(defined_vars))

    # Find HTML files
    html_files = sorted(proto_dir.glob("*.html"))
    if not html_files:
        result.add_warning(
            "NO_HTML_FILES",
            f"No *.html files found in {proto_dir}",
        )
        return result

    # Validate each HTML file
    for html_file in html_files:
        html_text = html_file.read_text(encoding="utf-8", errors="ignore")
        fname = html_file.name

        # --- Check 1: Undefined CSS classes ---
        for cls, lineno in _extract_html_classes(html_text):
            if cls in IGNORED_CLASSES or cls in defined_classes:
                continue
            # Check known mistakes
            if cls in KNOWN_MISTAKES:
                result.add_error(
                    "CLASS_WRONG_NAME",
                    f'{fname}: class "{cls}" is a known mistake',
                    file=str(html_file),
                    line=lineno,
                    suggestion=f'Use "{KNOWN_MISTAKES[cls]}" instead',
                )
            else:
                result.add_error(
                    "CLASS_UNDEFINED",
                    f'{fname}: class "{cls}" not defined in anta-prototype.css',
                    file=str(html_file),
                    line=lineno,
                    suggestion="Check SKILL.md Component Catalog for correct class name",
                )

        # --- Check 2: Undefined CSS variables ---
        for var_name, lineno in _extract_html_variables(html_text):
            if var_name in defined_vars:
                continue
            result.add_error(
                "VAR_UNDEFINED",
                f'{fname}: CSS variable "--{var_name}" not defined in :root',
                file=str(html_file),
                line=lineno,
                suggestion="Check anta-prototype.css :root for valid variable names",
            )

        # --- Check 3: Card body wrapping ---
        # .anta-card should contain .anta-card-body (or variant like --compact)
        # Find cards that have no card-body descendant at all
        card_starts = [m for m in re.finditer(r'class="[^"]*\banta-card\b(?!-)[^"]*"', html_text)]
        for m in card_starts:
            # Look ahead ~500 chars for any anta-card-body variant
            window = html_text[m.end():m.end() + 500]
            if not re.search(r'class="[^"]*\banta-card-body\b', window):
                lineno = html_text.count("\n", 0, m.start()) + 1
                result.add_warning(
                    "CARD_BODY_MISSING",
                    f"{fname}: .anta-card may be missing .anta-card-body wrapper",
                    file=str(html_file),
                    line=lineno,
                    suggestion='Wrap content in <div class="anta-card-body">...</div>',
                )

        # --- Check 4: Tab panel hidden attribute ---
        # Tab panels should use .anta-visible class, NOT hidden attribute
        for m in re.finditer(r'<[^>]*data-tab-panel="[^"]*"[^>]*>', html_text):
            snippet = m.group(0)
            if re.search(r'\bhidden\b', snippet):
                lineno = html_text.count("\n", 0, m.start()) + 1
                result.add_error(
                    "TAB_PANEL_HIDDEN",
                    f'{fname}: data-tab-panel uses "hidden" attribute',
                    file=str(html_file),
                    line=lineno,
                    suggestion="Remove hidden attribute. Use .anta-visible on the active panel instead.",
                )

        # --- Check 5: CSS and JS link references ---
        if '<link' in html_text and 'anta-prototype.css' not in html_text:
            result.add_warning(
                "CSS_LINK_MISSING",
                f"{fname}: no reference to anta-prototype.css in <head>",
                file=str(html_file),
            )
        if 'prototype-interactions.js' not in html_text:
            result.add_warning(
                "JS_LINK_MISSING",
                f"{fname}: no reference to prototype-interactions.js before </body>",
                file=str(html_file),
            )

    return result


def find_targets(root: Path) -> list:
    """For __dir__ protocol: find prototype directories to validate."""
    targets = []
    # Look for prototypes/ directory in typical locations
    for candidate in [
        root / "aidlc-docs" / "inception" / "prototypes",
        root / "prototypes",
        root,
    ]:
        if candidate.is_dir() and list(candidate.glob("*.html")):
            targets.append(candidate)
            break
    return targets


if __name__ == "__main__":
    if len(_sys.argv) < 2:
        print("Usage: python validate_html_prototype.py <prototypes_directory>")
        _sys.exit(1)
    target = _Path(_sys.argv[1])
    if not target.exists():
        print(f"ERROR: {target} does not exist")
        _sys.exit(1)
    # Directory-level validator — validate the entire prototypes folder at once
    result = validate(str(target))
    result.print_report()
    _sys.exit(0 if result.passed else 1)
