import logging
import tomllib
from pathlib import Path


def _find_config(path: Path | None = None) -> Path | None:
    """Recursively walk up to root from current working dir to find pyproject.toml"""
    if path is None:
        path = Path.cwd()
    if str(path) == path.root:
        logging.debug("No pyproject.toml found.")
        return None
    config_path = path / "pyproject.toml"
    if config_path.exists():
        return config_path
    else:
        _find_config(path.parent)


def _read_config() -> dict:
    path = _find_config()
    if path is None:
        return {}
    with open(path, "rb") as file:
        config = tomllib.load(file)
    try:
        return config["tool"]["pytest-approval"]
    except KeyError:
        logging.debug("No configuration table found.")
        return {}
