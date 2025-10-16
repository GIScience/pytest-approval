from pathlib import Path
from PIL import Image

import pytest

from pytest_approval import verify_image
from pytest_approval.definitions import BINARY_EXTENSIONS

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_image_bytes(extension):
    with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
        image = file.read()

    assert verify_image(image, extension=extension)



@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_image_pil(extension):
    image = Image.open(FIXTURE_DIR / f"binary{extension}")
    assert verify_image(image, extension=extension)
