import filecmp
from pathlib import Path
import logging

from pytest_approval.definitions import BINARY_EXTENSIONS


def compare_files(received: Path, approved: Path) -> bool:
    logging.debug(f"Compare {received} with {approved}.")
    if filecmp.cmp(received, approved, shallow=False):
        return True
    elif received.suffix not in BINARY_EXTENSIONS:
        return approved.read_text() == received.read_text()
    else:
        return False


def compare_image_contents_only(received: Path, approved: Path) -> bool:
    """Compare image contents without metadata."""
    try:
        import numpy
        from PIL import Image
    except ImportError as error:
        raise RuntimeError(
            'To use content_only, please install "pytest-approval[image]"'
            + '\n\n\tpip install "pytest-approval[image]"'
        ) from error
    received_image = Image.open(received)
    approved_image = Image.open(approved)
    return bool((numpy.array(received_image) == numpy.array(approved_image)).all())
