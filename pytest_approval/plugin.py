import logging

import pytest

from pytest_approval import main

node_ids = []
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

@pytest.hookimpl
def pytest_collection_modifyitems(items):
    global node_ids
    node_ids.extend(items)


def pytest_sessionfinish(session, exitstatus):
    """Cleanup unused approval files."""
    if exitstatus != 0:
        return
    config = session.config
    args = config.invocation_params.args
    if args:
        logging.debug("Specific tests/files were targeted. Abort cleanup.")
        return
    else:
        logging.debug("Whole test suite has been targeted. Start cleanup.")
    # TODO:
    # 1. Search for all approve/received files
    # 2. Generate file names for each node_id
    # 3. Delete all approved/received files (1)
    # which are not part of generated files names (2)
