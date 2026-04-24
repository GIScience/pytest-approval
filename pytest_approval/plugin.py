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


def pytest_configure(config):
    main.ROOT_DIR = config.rootpath
    main.AUTO_APPROVE = config.getoption("--auto-approve")
    approvals_dir = CONFIG.get("approvals-dir", None)
    if approvals_dir is not None:
        main.APPROVALS_DIR = approvals_dir
        approved_dir_path = Path(main.ROOT_DIR) / Path(main.APPROVALS_DIR)
        approved_dir_path.mkdir(parents=True, exist_ok=True)
