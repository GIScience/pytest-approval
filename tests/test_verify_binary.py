from pathlib import Path

import pytest

from pytest_approval import verify_binary
from pytest_approval.definitions import (
    BINARY_EXTENSIONS,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_binary(extension):
    with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
        data = file.read()

    assert verify_binary(data, extension=extension)
