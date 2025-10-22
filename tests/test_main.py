import logging
import re
from pathlib import Path

import pytest

from pytest_approval import verify
from pytest_approval.definitions import REPORTERS_TEXT
from pytest_approval.main import _name

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def approved(monkeypatch):
    monkeypatch.setattr("pytest_approval.main._count", lambda _: "")
    received, approved = _name()
    with open(approved, "w") as file:
        file.write("Hello World!\n")
    yield approved
    received.unlink(missing_ok=True)
    approved.unlink(missing_ok=True)


@pytest.fixture
def approved_different(monkeypatch):
    monkeypatch.setattr("pytest_approval.main._count", lambda _: "")
    _, approved = _name()
    with open(approved, "w") as file:
        file.write("hello world")
    yield approved


@pytest.fixture
def path(monkeypatch):
    monkeypatch.setattr("pytest_approval.main._count", lambda _: "")
    _, approved = _name()
    yield approved
    approved.unlink(missing_ok=True)


@pytest.mark.parametrize("string", ("Hello World!", "(id:(node/1, way/2))"))
def test_verify_string(string):
    assert verify(string)


def test_verify_multiple_calls():
    """Test multiple calls to verify. File names should be numbered."""
    assert verify("foo")
    assert verify("bar")


# @pytest.mark.parametrize("reporter", REPORTERS_TEXT[:-1])
# @pytest.mark.parametrize(
#     "string",
#     ("", ":*?<>|\t\n\r\x0b\x0c"),
# )
# def test_verify_string(reporter, string, monkeypatch):
#     monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", [reporter])
#     assert verify(string)


@pytest.mark.parametrize(
    "reporter",
    (REPORTERS_TEXT[0], REPORTERS_TEXT[2], REPORTERS_TEXT[3]),
)
def test_verify_string_all_reporter(reporter, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", [reporter])
    assert verify("Hello World!")


def test_verify_gnu_diff_tools_approver(monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", [REPORTERS_TEXT[-1]])
    with pytest.raises(AssertionError) as error:
        assert verify("Hello World!")
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", REPORTERS_TEXT)
    pattern = r"^\t\/.*\/([^\/]*(received|approved)\.txt)$"
    replacement = r"\t\1"
    error_text = re.sub(pattern, replacement, str(error.value), flags=re.MULTILINE)
    assert verify(error_text)


@pytest.mark.usefixtures("approved")
def test_verify_approved_equal(fake_process):
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is True
    assert fake_process.call_count(["meld", fake_process.any()]) == 0


@pytest.mark.usefixtures("approved")
def test_verify_approved_equal_report_always(fake_process):
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!", report_always=True) is True
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


@pytest.mark.usefixtures("approved_different")
def test_verify_approved_different(fake_process, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is False
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


def test_verify_approved_none(fake_process, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is False
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


def test_verify_different_returncode_127(fake_process, caplog, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    caplog.set_level(logging.DEBUG)
    fake_process.register_subprocess(
        ["meld", fake_process.any()],
        returncode=127,
    )
    fake_process.register_subprocess(
        ["pycharm", fake_process.any()],
        returncode=0,
    )
    assert verify("Hello World!") is False
    assert "Failed to run command" in caplog.text
    assert fake_process.call_count(["meld", fake_process.any()]) == 1
    assert fake_process.call_count(["pycharm", fake_process.any()]) == 1


def test_auto_approval(monkeypatch, path):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", True)
    assert not path.exists()
    assert verify("new content")
    assert path.exists()
