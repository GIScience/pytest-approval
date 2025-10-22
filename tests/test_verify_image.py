from pathlib import Path

import pytest
from PIL import Image

from pytest_approval import verify_image, verify_image_pillow
from pytest_approval.definitions import BINARY_EXTENSIONS

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_image_bytes(extension):
    with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
        image = file.read()

    assert verify_image(image, extension=extension)


@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_image_pillow(extension):
    image = Image.open(FIXTURE_DIR / f"binary{extension}")
    assert verify_image_pillow(image, extension=extension, content_only=True)
