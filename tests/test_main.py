import logging
import os
import re
from pathlib import Path

import pytest

from pytest_approval import scrub, verify
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


def test_verify_string_scrub_datetime():
    example = "2021-01-01T00:00:00+00:00"
    string = "Some text with datetime string 2021-01-01T00:00:00+00:00..."
    scrub_datetime = scrub.get_datetime_scrubber(example)
    assert verify(string, scrub=scrub_datetime)


def test_verify_string_scrub_uuid():
    string = "Some text with uuid string 27de4925-c261-4e8f-973d-74213004b27d..."
    scrub_uuid = scrub.get_uuid_scrubber()
    assert verify(string, scrub=scrub_uuid)


def test_verify_string_scrub_multiple():
    scrub_uuid = scrub.get_uuid_scrubber()
    scrub_datetime = scrub.get_datetime_scrubber("2020-02-02")
    assert verify(
        "27de4925-c261-4e8f-973d-74213004b27d and 2020-02-02",
        scrub=(scrub_uuid, scrub_datetime),
    )


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


def test_verify_gnu_diff_tools_approver(monkeypatch, capsys: pytest.CaptureFixture):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", [REPORTERS_TEXT[-1]])
    assert not verify("Hello World!")
    stdout, _ = capsys.readouterr()
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", REPORTERS_TEXT)
    pattern = r"^\t\/.*\/([^\/]*(received|approved)\.txt)$"
    replacement = r"\t\1"
    log = re.sub(pattern, replacement, stdout, flags=re.MULTILINE)
    assert verify(log)


@pytest.mark.usefixtures("approved")
def test_verify_approved_equal(fake_process, monkeypatch):
    monkeypatch.delenv("CI", raising=False)
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is True
    assert fake_process.call_count(["meld", fake_process.any()]) == 0


@pytest.mark.usefixtures("approved")
def test_verify_approved_equal_report_always(fake_process, monkeypatch):
    fake_process.register_subprocess(["meld", fake_process.any()])
    monkeypatch.delenv("CI", raising=False)
    assert verify("Hello World!", report_always=True) is True
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


@pytest.mark.usefixtures("approved_different")
def test_verify_approved_different(fake_process, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    monkeypatch.delenv("CI", raising=False)
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is False
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


def test_verify_approved_none(fake_process, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    monkeypatch.delenv("CI", raising=False)
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is False
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


def test_verify_different_returncode_127(fake_process, caplog, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    monkeypatch.delenv("CI", raising=False)
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


@pytest.mark.skipif(
    os.environ.get("CI") is not None,
    reason="Skipping because test mocks CI environment",
)
def test_verify_ci(monkeypatch, capsys: pytest.CaptureFixture):
    """In CI gnu diff reporter should be used."""
    with monkeypatch.context() as m:
        m.setenv("CI", "Jenkins")
        assert not verify("Hello World!")
    stdout, _ = capsys.readouterr()
    # replace host file path
    pattern = r"^\t\/.*\/([^\/]*(received|approved)\.txt)$"
    replacement = r"\t\1"
    error_text = re.sub(pattern, replacement, stdout, flags=re.MULTILINE)
    assert verify(error_text)
