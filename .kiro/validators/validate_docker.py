"""validate_docker — Validate Docker and docker-compose configuration."""

import logging
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from __init__ import ValidationResult, run_validator_cli

logger = logging.getLogger(__name__)

def _project_root(path: Path) -> Path:
    """Get project root directory from file or directory path."""
    return path if path.is_dir() else path.parent


def validate(file_path: str) -> ValidationResult:
    """Validate Docker and docker-compose files in project."""
    root = _project_root(Path(file_path))
    result = ValidationResult(validator="validate_docker", target=str(root))
    logger.debug("Validating %s", file_path)

    if not root.exists():
        result.add_error("DOCKER_FILE", "Target project path does not exist.")
        return result

    dockerfile = root / "Dockerfile_local"
    compose = root / "docker-compose.yml"

    if not dockerfile.exists():
        result.add_error("DOCKER_FILE", "Project should include Dockerfile_local.")
    if not compose.exists():
        result.add_error("DOCKER_COMPOSE", "Project should include docker-compose.yml.")

    compose_text = compose.read_text(encoding="utf-8", errors="ignore") if compose.exists() else ""
    if compose.exists() and "antamina-network" not in compose_text:
        result.add_error("DOCKER_NETWORK", "docker-compose.yml should define or use antamina-network.")

    docker_text = dockerfile.read_text(encoding="utf-8", errors="ignore") if dockerfile.exists() else ""
    if dockerfile.exists():
        if not re.search(r"^\s*FROM\s+.+\s+AS\s+build\b", docker_text, re.IGNORECASE | re.MULTILINE):
            result.add_warning("DOCKER_MULTI_STAGE", "Dockerfile_local should use a build stage.")
        elif not re.search(r"^\s*FROM\s+.+\s+AS\s+(runtime|final)\b", docker_text, re.IGNORECASE | re.MULTILINE):
            result.add_warning("DOCKER_MULTI_STAGE", "Dockerfile_local should use a runtime/final stage.")
        if "nuget.config" not in docker_text:
            result.add_warning("DOCKER_NUGET_CONFIG", "Dockerfile_local should copy nuget.config.")
        if "ENTRYPOINT" not in docker_text:
            result.add_warning("DOCKER_ENTRYPOINT", "Dockerfile_local should define an ENTRYPOINT.")

    logger.debug("Validation complete: %s — %d errors, %d warnings", file_path, len(result.errors), len(result.warnings))
    return result


if __name__ == "__main__":
    run_validator_cli(validate, "validate_docker", ["Dockerfile_local", "docker-compose.yml"])
