import json
import logging
import os
import shutil
import subprocess
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


def verify(
    data: Any,
    *,
    extension: str = ".txt",
) -> bool:
    return _verify(data, extension)


def verify_binary(
    data: Any,
    *,
    extension: Literal[BINARY_EXTENSIONS],
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
        with open(received, "wb") as file:
            file.write(data)
        if not approved.exists():
            empty_file = Path(BASE_DIR / "empty_files" / "empty").with_suffix(
                approved.suffix
            )
            try:
                shutil.copy(empty_file, approved)
            except FileNotFoundError:
                raise ValueError(
                    "Extension '{0}' not supported. ".format(approved.suffix)
                    + "Extension for binary verification must be one of: {0}".format(
                        BINARY_EXTENSIONS
                    )
                )
    else:
        if len(data) == 0 or data[-1] != "\n":
            data = data + "\n"
        received.write_text(data)
        if not approved.exists():
            approved.touch()


def _name(extension=".txt") -> tuple[Path]:
    # TODO: support base dir (then rewrite tests to use tmp_dir)
    # TODO: support postfix (write test with multiple calls to verify)
    # Write paramatrized tests
    # TODO: Try out with xdist
    node_id = os.environ["PYTEST_CURRENT_TEST"]
    parts = node_id.split("::")
    parts[-1] = parts[-1].replace("/", "--")
    file_path = (
        "::".join(parts)
        .replace(" (call)", "")
        .replace(" (setup)", "")
        .replace(" (teardown)", "")
        .replace("::", "--")
    )
    chars = [
        ":",
        "*",
        "?",
        "<",
        ">",
        "|",
        r"\\",
        r"\t",
        r"\n",
        r"\r",
        r"\x0b",
        r"\x0c",
    ]
    for c in chars:
        file_path = file_path.replace(c, "-")
    received = file_path + ".received" + extension
    approved = file_path + ".approved" + extension
    return (
        Path(received).resolve(),
        Path(approved).resolve(),
    )


def _report(received: Path, approved: Path):
    if received.suffix in BINARY_EXTENSIONS:
        reporters = REPORTERS_BINARY
    else:
        reporters = REPORTERS_TEXT
    for command in reporters:
        command = [c.replace("%received", str(received)) for c in command]
        command = [c.replace("%approved", str(approved)) for c in command]
        try:
            completed_process = subprocess.run(
                command,
                capture_output=True,
                check=False,
            )
            if completed_process.returncode == 127:  # command not found
                raise FileNotFoundError()
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
    raise FileNotFoundError("No working approver could be found.")
