import logging

from pytest_approval.main import verify, verify_binary

__all__ = ("verify", "verify_binary")

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
)
