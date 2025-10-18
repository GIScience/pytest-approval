from pathlib import Path

import pytest

from pytest_approval import verify_binary
from pytest_approval.definitions import (
    BINARY_EXTENSIONS,
    REPORTERS_BINARY,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures"


# TODO read empty files for extension and verify it:
@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_binary(extension, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.REPORTERS_BINARY", [REPORTERS_BINARY[1]])
    with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
        data = file.read()

    assert verify_binary(data, extension=extension)
