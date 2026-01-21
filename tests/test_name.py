import os
import platform

import pytest

from pytest_approval.main import _name


def get_filename_limit():
    system = platform.system()

    if system == "Windows":
        return 255  # NTFS file name limit
    elif system in ("Linux", "Darwin"):  # Darwin = macOS
        try:
            return os.pathconf(".", "PC_NAME_MAX")
        except (AttributeError, OSError, ValueError):
            return 255  # Fallback
    else:
        return 255  # Generic fallback for other OSes


def test_name():
    path = _name()
    name = tuple(p.name for p in path)
    assert name[0] == "test_name.py--test_name.received.txt"
    assert name[1] == "test_name.py--test_name.approved.txt"


def test_name_two_calls_numbered_name():
    path = _name()
    name = tuple(p.name for p in path)
    assert name[0] == "test_name.py--test_name_two_calls_numbered_name.received.txt"
    assert name[1] == "test_name.py--test_name_two_calls_numbered_name.approved.txt"
    path = _name()
    name = tuple(p.name for p in path)
    assert name[0] == "test_name.py--test_name_two_calls_numbered_name.2.received.txt"
    assert name[1] == "test_name.py--test_name_two_calls_numbered_name.2.approved.txt"


def test_name_with_a_long_name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx():
    # fmt: off
    path = _name()
    name = tuple(p.name for p in path)
    assert name[0] == "test_name.py--test_name_with_a_long_name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.received.txt"  # noqa
    assert name[1] == "test_name.py--test_name_with_a_long_name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.approved.txt"  # noqa
    # fmt: on


@pytest.mark.parametrize("param", ["a" * (get_filename_limit() + 1)])
def test_name_with_too_long_parameter_name(param):
    # fmt: off
    path = _name()
    name = tuple(p.name for p in path)
    assert name[0] == "test_name.py--test_name_with_too_long_parameter_name[2960995929].received.txt"  # noqa
    assert name[1] == "test_name.py--test_name_with_too_long_parameter_name[2960995929].approved.txt"  # noqa
    # fmt: on
