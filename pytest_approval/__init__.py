from contextlib import suppress

from pytest_approval.main import (
    verify,
    verify_binary,
    verify_image,
    verify_json,
)
from pytest_approval.scrub import get_datetime_scrubber, get_uuid_scrubber

__all__ = (
    "get_datetime_scrubber",
    "get_uuid_scrubber",
    "verify",
    "verify_binary",
    "verify_image",
    "verify_json",
)


with suppress(ImportError):
    from pytest_approval.main import verify_image_pillow

    __all__ = (*__all__, "verify_image_pillow")


with suppress(ImportError):
    from pytest_approval.main import verify_plotly

    __all__ = (*__all__, "verify_plotly")
