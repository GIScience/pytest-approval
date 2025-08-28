from contextlib import suppress
from pathlib import Path

from pytest_approval.config import _read_config

BASE_DIR = Path(__file__).parent.resolve()

REPORTERS_TEXT: list[list[str]] = [
    [
        "meld",
        "%received",
        "%approved",
    ],
    [
        "pycharm",
        "diff",
        "%received",
        "%approved",
    ],
    [
        "/usr/bin/flatpak",
        "run",
        "com.jetbrains.PyCharm-Community",
        "diff",
        "%received",
        "%approved",
    ],
    [
        "/usr/bin/code",
        "--new-window",
        "--wait",
        "--diff",
        "%received",
        "%approved",
    ],
    [
        "/usr/bin/open",
        # -W: Wait until the application is closed
        "-W",
        # -n: new instance
        "-n",
        # -a: application
        "-a",
        "/Applications/PyCharm Professional Edition.app/Contents/MacOS/pycharm",
        "--args",
        "diff",
        "%received",
        "%approved",
    ],
    [
        "/usr/bin/open",
        # -W: Wait until the application is closed
        "-W",
        # -n: New instance
        "-n",
        # -a: Application
        "-a",
        "/Applications/PyCharm CE.app/Contents/MacOS/pycharm",
        "--args",
        "diff",
        "%received",
        "%approved",
    ],
    [
        "/usr/bin/open",
        # -W: Wait until the application is closed
        "-W",
        # -n: New instance
        "-n",
        # -a: Application
        "-a",
        "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",
        "--args",
        "--new-window",
        "--wait",
        "--diff",
        "%received",
        "%approved",
    ],
    [
        "diff",
        "--unified",
        "--color",
        "--suppress-common-lines",
        "--label",
        "received",
        "--label",
        "approved",
        "%received",
        "%approved",
    ],
]


REPORTERS_BINARY: list[list[str]] = [
    [
        "pycharm",
        "diff",
        "%received",
        "%approved",
    ],
    [
        "/usr/bin/flatpak",
        "run",
        "com.jetbrains.PyCharm-Community",
        "diff",
        "%received",
        "%approved",
    ],
    [
        "diff",
        "--unified",
        "--color",
        "--suppress-common-lines",
        "--label",
        "received",
        "--label",
        "approved",
        "%received",
        "%approved",
    ],
]

BINARY_EXTENSIONS: list[str] = [
    # "7z",
    # "7zip",
    # "avif",
    # "bmp",
    # "bz2",
    # "bzip2",
    # "dds",
    # "dib",
    # "docx",
    # "emf",
    # "exif",
    # "gif",
    # "gz",
    # "gzip",
    # "heic",
    # "heif",
    # "ico",
    # "j2c",
    # "jfif",
    # "jp2",
    # "jpc",
    # "jpe",
    ".jpeg",
    ".jpg",
    # "jxr",
    # "nupkg",
    # "odp",
    # "ods",
    # "odt",
    # "pbm",
    # "pcx",
    # "pdf",
    # "pgm",
    ".png",
    # "ppm",
    # "pptx",
    # "rle",
    # "rtf",
    # "tar",
    # "tga",
    # "tif",
    # "tiff",
    # "wdp",
    # "webp",
    # "wmp",
    # "xlsx",
    # "xz",
    # "zip",
]

CONFIG = _read_config()

with suppress(KeyError):
    REPORTERS_TEXT = list(set(CONFIG["reporters"] + REPORTERS_TEXT))
