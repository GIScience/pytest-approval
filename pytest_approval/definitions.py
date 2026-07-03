from pathlib import Path

from pytest_approval.config import _read_config

BASE_DIR = Path(__file__).parent.resolve()

# Order matters: First working reporter is found by going through this list one-by-one
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
        "image": False,
        "pdf": False,
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
                "flatpak",
                "run",
                "com.jetbrains.PyCharm-Professional",
                "diff",
                "%received",
                "%approved",
            ],
            [
                "/usr/bin/snap",
                "run",
                "pycharm",
                "diff",
                "%received",
                "%approved",
            ],
            [
                "snap",
                "run",
                "pycharm",
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
        "binary": False,
        "image": True,
        "pdf": True,
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
        "binary": False,
        "image": True,
        "pdf": True,
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
        "image": True,
        "pdf": True,
    },
}

# Supported binary extensions.
# Support depends on an empty file being present.
BINARY_EXTENSIONS: list[str] = [
    ".jpeg",
    ".jpg",
    ".parquet",
    # ".pdf",
    ".png",
]

CONFIG = _read_config()

# with suppress(KeyError):
#     REPORTERS = list(set(CONFIG["reporters"] + REPORTERS))
