from pathlib import Path

from pytest_approval.config import _read_config

BASE_DIR = Path(__file__).parent.resolve()

# Order matters: First working reporter is found by going thorugh this list one-by-one
REPORTERS = {
    "meld": {
        "commands": [
            [
                "meld",
                "%received",
                "%approved",
            ]
        ],
        "binary": False,
    },
    "pycharm": {
        "commands": [
            [
                "pycharm",
                "diff",
                "%received",
                "%approved",
            ],
            [
                str(Path.home().resolve())
                + "/.local/share/JetBrains/Toolbox/scripts/pycharm",
                "diff",
                "%received",
                "%approved",
            ],
            [
                "/usr/bin/flatpak",
                "run",
                "com.jetbrains.PyCharm-Professional",
                "diff",
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
                "PyCharm.app",
                "--args",
                "diff",
                "%received",
                "%approved",
            ],
            # TODO: https://snapcraft.io/pycharm
            # TODO: https://www.jetbrains.com/help/pycharm/working-with-the-ide-features-from-command-line.html#toolbox
        ],
        "binary": True,
    },
    "code": {
        "commands": [
            [
                "code",
                "--new-window",
                "--wait",
                "--diff",
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
        ],
        "binary": True,
    },
    "diff": {
        "commands": [
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
        ],
        "binary": True,  # used as fallback reporter
    },
}

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

# with suppress(KeyError):
#     REPORTERS = list(set(CONFIG["reporters"] + REPORTERS))
