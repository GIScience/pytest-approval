import pytest

from pytest_approval.main import _name


@pytest.fixture
def path(monkeypatch):
    monkeypatch.setattr("pytest_approval.main._count", lambda _: "")
    _, approved = _name()
    yield approved
    approved.unlink(missing_ok=True)
