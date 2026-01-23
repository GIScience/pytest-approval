import os
import re
from pathlib import Path

import pytest

from pytest_approval import verify, verify_binary
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


@pytest.mark.skipif(
    os.environ.get("CI") is not None,
    reason="Skipping because test mocks CI environment",
)
@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_binary_ci(extension, monkeypatch, capsys: pytest.CaptureFixture):
    """In CI gnu diff reporter should be used."""
    with monkeypatch.context() as m:
        m.setenv("CI", "Jenkins")
        with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
            data = file.read()
        assert not verify_binary(data, extension=extension)
    stdout, _ = capsys.readouterr()
    # replace host file path
    pattern = r"^\t\/.*\/([^\/]*(received|approved)\{0})$".format(extension)
    replacement = r"\t\1"
    text = re.sub(pattern, replacement, stdout, flags=re.MULTILINE)
    assert verify(text)
