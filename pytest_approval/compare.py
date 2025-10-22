import filecmp
import logging
from pathlib import Path

from pytest_approval.definitions import BINARY_EXTENSIONS

logger = logging.getLogger(__name__)


def compare_files(received: Path, approved: Path) -> bool:
    logger.debug(f"Compare {received} with {approved}.")
    if filecmp.cmp(received, approved, shallow=False):
        return True
    elif received.suffix not in BINARY_EXTENSIONS:
        return approved.read_text() == received.read_text()
    else:
        return False


def compare_files_shallow(received: Path, approved: Path) -> bool:
    logger.debug(f"Compare {received} with {approved}.")
    if filecmp.cmp(received, approved, shallow=True):
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
    received_array = numpy.array(received_image)
    approved_array = numpy.array(approved_image)
    return numpy.array_equiv(received_array, approved_array)
