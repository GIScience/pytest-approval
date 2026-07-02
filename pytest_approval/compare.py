import filecmp
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def compare_text(received: Path, approved: Path) -> bool:
    logger.debug(f"Compare {received} with {approved}.")
    return approved.read_text() == received.read_text()


def compare_files(received: Path, approved: Path) -> bool:
    logger.debug(f"Compare {received} with {approved}.")
    return filecmp.cmp(received, approved, shallow=False)


def compare_image_contents_only(received: Path, approved: Path) -> bool:
    """Compare image contents without metadata."""
    logger.debug(f"Compare {received} with {approved}.")
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
