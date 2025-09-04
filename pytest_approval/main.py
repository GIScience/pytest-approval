import json
import logging
import os
import shutil
import subprocess
import zlib
from pathlib import Path
from typing import Any, Callable, Literal

from pytest_approval.compare import compare_files, compare_image_contents_only
from pytest_approval.definitions import (
    BASE_DIR,
    BINARY_EXTENSIONS,
    REPORTERS_BINARY,
    REPORTERS_TEXT,
)
from pytest_approval.utils import sort_dict

# will be instantiated during pytest configuration by plugin.py
ROOT_DIR: str = ""
APPROVED_DIR: str = ""
AUTO_APPROVE: bool = False

NAMES = []


def verify(
    data: Any,
    *,
    extension: str = ".txt",
) -> bool:
    return _verify(data, extension)


def verify_binary(
    data: Any,
    *,
    extension: Literal[".jpg", ".jpeg", ".png"],
) -> bool:
    return _verify(data, extension)


def verify_image(
    data: Any,
    *,
    extension: Literal[".jpg", ".jpeg", ".png"],
    content_only: bool = False,
) -> bool:
    """Verify image.

    Args:
        content_only: only compare content without metadata.
    """
    if content_only:
        return _verify(data, extension, compare=compare_image_contents_only)
    return _verify(data, extension)


def verify_json(
    data: str | dict,
    *,
    extension: Literal[".json"] = ".json",
    sort: bool = False,
) -> bool:
    if isinstance(data, str):
        data = json.loads(data)
    if sort:
        data = sort_dict(data)
    data = json.dumps(data, indent=True)
    return _verify(data, extension)


def _verify(data: Any, extension: str, compare: Callable = compare_files) -> bool:
    received, approved = _name(extension)
    _write(data, received, approved)
    if AUTO_APPROVE:
        shutil.copyfile(received, approved)
    if compare(received, approved):
        received.unlink()
        return True
    else:
        _report(received, approved)
        if compare(received, approved):
            received.unlink()
            return True
        else:
            return False


def _write(data, received, approved):
    """Write received to disk and create empty approved file if not exists."""
    if received.suffix in BINARY_EXTENSIONS:
        _write_binary(data, received, approved)
    else:
        _write_text(data, received, approved)


def _write_binary(data, received, approved):
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


def _write_text(data, received, approved):
    if len(data) == 0 or data[-1] != "\n":
        data = data + "\n"
    received.write_text(data)
    if not approved.exists():
        approved.touch()


def _name(extension=".txt") -> tuple[Path, Path]:
    # TODO: support base dir (then rewrite tests to use tmp_dir)
    # TODO: support postfix (write test with multiple calls to verify)
    # TODO: Try out with xdist
    node_id = os.environ["PYTEST_CURRENT_TEST"]
    if "[" in node_id and "]" in node_id:
        # TODO: Only use hash if params are loo long or special chars are presenet
        start = node_id.index("[") + 1
        end = node_id.index("]")
        params = node_id[start:end]
        hash = str(zlib.crc32(params.encode("utf-8")))
    else:
        params = ""
        hash = ""
    file_path = (
        node_id.replace(" (call)", "")
        .replace(" (setup)", "")
        .replace(" (teardown)", "")
        .replace("::", "--")
        .replace(params, hash)
    )
    count = _count(file_path)
    if APPROVED_DIR:
        file_path = Path(file_path)
        # find common parents between approved dir and file path, both
        # relative to pytest root, and remove them
        for i, part in enumerate(Path(APPROVED_DIR).parts):
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
        Path(ROOT_DIR) / Path(APPROVED_DIR) / Path(received),
        Path(ROOT_DIR) / Path(APPROVED_DIR) / Path(approved),
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
            logging.debug(f"Failed to run command `{' '.join(command)}` as approver.")
            continue
        if completed_process.returncode == 0:
            return
        elif completed_process.returncode == 1:
            msg = (
                "Received is different from approved.\n"
                + f"To approve run mv --force {received} {approved}\n"
            )
            raise AssertionError(msg + completed_process.stdout.decode("utf-8"))
        else:
            continue
    raise FileNotFoundError("No working approver could be found.")  # noqa: TRY003


def cleaner(path: Path):
    path = Path(path)
    if path.is_dir():
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                #filename = str(Path(filename).name)
                if ".approved." in filenames and filename not in NAMES:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
