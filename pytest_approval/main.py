import json
import logging
import os
import shutil
import subprocess
import zlib
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal

if TYPE_CHECKING:
    # Always true for type checker. Always false during runtime.
    from PIL import Image

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from pytest_approval.compare import compare_files, compare_image_contents_only
from pytest_approval.definitions import (
    BASE_DIR,
    BINARY_EXTENSIONS,
    REPORTERS_BINARY,
    REPORTERS_TEXT,
)
from pytest_approval.utils import sort_dict

logger = logging.getLogger(__name__)

# will be instantiated during pytest configuration by plugin.py
ROOT_DIR: str = ""
APPROVALS_DIR: str = ""
AUTO_APPROVE: bool = False

NAMES = []


class NoApproverFoundError(FileNotFoundError):
    def __init__(self):
        super().__init__("No working approver could be found.")


def verify(data: str, *, extension: str = ".txt", report_always: bool = False) -> bool:
    """Verify.

    Args:
        report_always: Always report even if received and approved are equal.
    """
    return _verify(data, extension, report_always)


def verify_binary(
    data: bytes,
    *,
    extension: Literal[".jpg", ".jpeg", ".png"],
    report_always: bool = False,
) -> bool:
    return _verify(data, extension, report_always)


def verify_image(
    data: bytes,
    *,
    extension: Literal[".jpg", ".jpeg", ".png"],
    report_always: bool = False,
    content_only: bool = False,
) -> bool:
    """Verify image.

    Args:
        content_only: only compare content without metadata.
    """
    if content_only:
        return _verify(
            data,
            extension,
            report_always,
            compare=compare_image_contents_only,
        )
    return _verify(data, extension, report_always)


if PIL_AVAILABLE:

    def _pillow_image_to_bytes(image: Image.Image, extension: str) -> bytes:
        buffer = BytesIO()
        format_ = extension.replace(".", "")
        if format_ == "jpg":
            format_ = "jpeg"
        image.save(buffer, format=format_)
        return buffer.getvalue()

    def verify_image_pillow(
        data: Image.Image,
        *,
        extension: Literal[".jpg", ".jpeg", ".png"],
        report_always: bool = False,
        content_only: bool = False,
    ) -> bool:
        """Verify pillow image.

        Args:
            content_only: only compare content without metadata.
        """
        raw = _pillow_image_to_bytes(data, extension)
        return verify_image(
            raw,
            extension=extension,
            report_always=report_always,
            content_only=content_only,
        )


def verify_json(
    data: str | dict | list | Any,
    *,
    extension: Literal[".json"] = ".json",
    report_always: bool = False,
    sort: bool = False,
) -> bool:
    """Verify as JSON.

    Accepts data as JSON string or JSON serializable object.
    """
    if isinstance(data, str):
        data = json.loads(data)
    if sort and isinstance(data, dict):
        data = sort_dict(data)
    elif sort and isinstance(data, list):
        data.sort()
    data = json.dumps(data, indent=True)
    return _verify(data, extension=extension, report_always=report_always)


def _verify(
    data: Any,
    extension: str,
    report_always: bool,
    compare: Callable = compare_files,
) -> bool:
    received, approved = _name(extension)
    _write(data, received, approved)
    if AUTO_APPROVE:
        shutil.copyfile(received, approved)
    if compare(received, approved) and not report_always:
        received.unlink()
        return True
    else:
        _report(received, approved)
        if compare(received, approved):
            received.unlink()
            return True
        else:
            return False


def _write(data, received: Path, approved: Path):
    """Write received to disk and create empty approved file if not exists."""
    received.parent.mkdir(exist_ok=True, parents=True)
    approved.parent.mkdir(exist_ok=True, parents=True)
    if received.suffix in BINARY_EXTENSIONS:
        _write_binary(data, received, approved)
    else:
        _write_text(data, received, approved)


def _write_binary(data, received: Path, approved: Path):
    with open(received, "wb") as file:
        file.write(data)
    if not approved.exists():
        empty_file = Path(BASE_DIR / "empty_files" / "empty").with_suffix(
            approved.suffix
        )
        try:
            shutil.copy(empty_file, approved)
        except FileNotFoundError as e:
            raise ValueError(
                "Extension '{0}' not supported. ".format(approved.suffix)
                + "Extension for binary verification must be one of: {0}".format(
                    BINARY_EXTENSIONS
                )
            ) from e


def _write_text(data, received: Path, approved: Path):
    if len(data) == 0 or data[-1] != "\n":
        data = data + "\n"
    received.write_text(data)
    if not approved.exists():
        approved.touch()


def _name(extension=".txt") -> tuple[Path, Path]:
    # TODO: Try out with xdist
    node_id = os.environ["PYTEST_CURRENT_TEST"]
    if "[" in node_id and "]" in node_id:
        # TODO: Only use hash if params are loo long or special chars are present
        start = node_id.index("[") + 1
        end = node_id.index("]")
        params = node_id[start:end]
        hash_ = str(zlib.crc32(params.encode("utf-8")))
    else:
        params = ""
        hash_ = ""
    file_path = (
        node_id.replace(" (call)", "")
        .replace(" (setup)", "")
        .replace(" (teardown)", "")
        .replace("::", "--")
        .replace(params, hash_)
    )
    count = _count(file_path)
    if APPROVALS_DIR:
        file_path = Path(file_path)
        # find common parents between approved dir and file path, both
        # relative to pytest root, and remove them
        for i, part in enumerate(Path(APPROVALS_DIR).parts):
            if part == file_path.parts[i]:
                continue
            else:
                break
        else:
            i = 0
        file_path = str(Path(*file_path.parts[i:]))
    received = file_path + count + ".received" + extension
    approved = file_path + count + ".approved" + extension
    return (
        Path(ROOT_DIR) / Path(APPROVALS_DIR) / Path(received),
        Path(ROOT_DIR) / Path(APPROVALS_DIR) / Path(approved),
    )


def _count(file_path: str) -> str:
    """Count generated names which are the same.

    This means `verify` has been called multiple times in one test function.
    """
    NAMES.append(file_path)
    count = NAMES.count(file_path)
    if count == 1:
        return ""
    else:
        return "." + str(count)


def _report(received: Path, approved: Path):
    if received.suffix in BINARY_EXTENSIONS:
        reporters = REPORTERS_BINARY
    else:
        reporters = REPORTERS_TEXT
    for command in reporters:
        command = [c.replace("%received", str(received)) for c in command]
        command = [c.replace("%approved", str(approved)) for c in command]
        try:
            completed_process = subprocess.run(  # noqa S603
                command,
                capture_output=True,
                check=False,
            )
            if completed_process.returncode == 127:  # command not found
                raise FileNotFoundError()  # noqa: TRY301
        except FileNotFoundError:
            logger.debug(f"Failed to run command `{' '.join(command)}` as approver.")
            continue
        if completed_process.returncode == 0:
            return
        elif completed_process.returncode == 1:
            msg = (
                "Received is different from approved:\n"
                + f"\t{received}\n\t{approved}\n"
            )
            raise AssertionError(msg + completed_process.stdout.decode("utf-8"))
        else:
            raise NoApproverFoundError()
