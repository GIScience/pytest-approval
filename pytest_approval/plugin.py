from pathlib import Path

from pytest_approval import main
from pytest_approval.definitions import CONFIG

auto_approve: bool = False


def pytest_addoption(parser):
    parser.addoption(
        "--auto-approve",
        action="store_true",
        help="Automatically approve every approval test",
    )
    parser.addoption(
        "--clean-unused",
        action="store_true",
        help="Remove all files in the approved directory, that are not used in this test run.",
    )


def pytest_configure(config):
    main.ROOT_DIR = config.rootpath
    main.AUTO_APPROVE = config.getoption("--auto-approve")
    main.CLEAN_UNUSED = config.getoption("--clean-unused")
    approved_dir = CONFIG.get("approved-dir", None)
    if approved_dir is not None:
        main.APPROVED_DIR = approved_dir
        approved_dir_path = Path(main.ROOT_DIR) / Path(main.APPROVED_DIR)
        approved_dir_path.mkdir(parents=True, exist_ok=True)

def pytest_sessionfinish(session, exitstatus):
    if main.CLEAN_UNUSED:
        main.cleaner(Path(main.ROOT_DIR) / Path(main.APPROVED_DIR))