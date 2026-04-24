from pathlib import Path
from typing import Iterable

import pytest
from pytest_nodeid_to_filepath import get_filepath


@pytest.fixture
def approved_path() -> Iterable[Path]:
    path = get_filepath(
        extension=".approved.txt", directory="tests/approvals", count=False
    )
    yield path
    path.unlink(missing_ok=True)


@pytest.fixture
def received_path() -> Iterable[Path]:
    path = get_filepath(
        extension=".received.txt", directory="test/approvals", count=False
    )
    yield path
    path.unlink(missing_ok=True)
