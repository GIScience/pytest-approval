from pathlib import Path

from pytest_approval import main

auto_approve: bool = False


def pytest_addoption(parser):
    parser.addoption(
        "--auto-approve",
        action="store_true",
        help="Automatically approve every approval test",
    )
    parser.addoption(
        "--approved-dir",
        action="store",
        default="",
        help="Directory for approved files (relative to pytest root.",
    )


def pytest_configure(config):
    main.ROOT_DIR = config.rootpath
    main.AUTO_APPROVE = config.getoption("--auto-approve")
    if approved_dir := config.getoption("--approved-dir", None):
        main.APPROVED_DIR = approved_dir
        approved_dir_path = Path(main.ROOT_DIR) / Path(main.APPROVED_DIR)
        approved_dir_path.mkdir(parents=True, exist_ok=True)
