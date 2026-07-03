import os
import re
from pathlib import Path

import pytest
from PIL import Image

from pytest_approval import verify_image, verify_image_pillow
from pytest_approval.main import verify

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("extension", [".jpeg", ".jpg", ".png"])
def test_verify_image_bytes(extension):
    with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
        image = file.read()

    assert verify_image(image, extension=extension)


@pytest.mark.parametrize("extension", [".jpeg", ".jpg", ".png"])
def test_verify_image_pillow(extension):
    image = Image.open(FIXTURE_DIR / f"binary{extension}")
    assert verify_image_pillow(image, extension=extension, content_only=True)


@pytest.mark.skipif(
    os.environ.get("CI") is not None,
    reason="Skipping because test mocks CI environment",
)
@pytest.mark.parametrize("extension", [".jpeg", ".jpg", ".png"])
def test_verify_image_ci(extension, monkeypatch, capsys: pytest.CaptureFixture):
    """In CI gnu diff reporter should be used."""
    with monkeypatch.context() as m:
        m.setenv("CI", "Jenkins")
        with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
            data = file.read()
        assert not verify_image(data, extension=extension)
    stdout, _ = capsys.readouterr()
    # replace host file path
    pattern = r"^\t\/.*\/([^\/]*(received|approved)\{0})$".format(extension)
    replacement = r"\t\1"
    text = re.sub(pattern, replacement, stdout, flags=re.MULTILINE)
    assert verify(text)
