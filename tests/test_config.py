from pathlib import Path

from pytest_approval import config


def test_find_config_none():
    assert config._find_config(Path("/")) is None


def test_find_config():
    assert config._find_config() == Path(__file__).parent.parent / "pyproject.toml"


def test_read_config():
    assert config._read_config() == {'approved-dir': 'tests/approved'}
