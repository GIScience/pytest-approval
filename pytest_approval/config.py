import logging
import tomllib
from pathlib import Path

logger = logging.getLogger(__name__)


def _find_config(path: Path | None = None) -> Path | None:
    """Recursively walk up to root from current working dir to find pyproject.toml"""
    if path is None:
        path = Path.cwd()
    if str(path) == path.root:
        logger.debug("No pyproject.toml found.")
        return None
    config_path = path / "pyproject.toml"
    if config_path.exists():
        return config_path
    else:
        return _find_config(path.parent)


def _read_config() -> dict:
    path = _find_config()
    if path is None:
        return {}
    with open(path, "rb") as file:
        config = tomllib.load(file)
    try:
        return config["tool"]["pytest-approval"]
    except KeyError:
        logger.debug("No configuration table found.")
        return {}
