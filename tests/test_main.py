import logging
from pathlib import Path

import pytest

from pytest_approval import verify, verify_binary, verify_json
from pytest_approval.definitions import (
    BINARY_EXTENSIONS,
    REPORTERS_BINARY,
    REPORTERS_TEXT,
)
from pytest_approval.main import _name

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def approved():
    received, approved = _name()
    with open(approved, "w") as file:
        file.write("Hello World!\n")
    yield approved
    try:
        received.unlink()
        approved.unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
def approved_different():
    received, approved = _name()
    with open(approved, "w") as file:
        file.write("hello world")
    yield approved


@pytest.mark.parametrize("string", ("Hello World!", "(id:(node/1, way/2))"))
def test_verify_string(string):
    assert verify(string)


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


@pytest.mark.parametrize(
    "json",
    (
        {"b": 100, "a": None},
        '{"b": 100, "a": null}',
    ),
)
def test_verify_json(json):
    assert verify_json(json)


def test_verify_json_sort():
    json = {"b": 100, "a": {"d": 10, "c": 10}}
    assert verify_json(json, sort=True)


# TODO read empty files for extension and verify it:
@pytest.mark.parametrize("extension", BINARY_EXTENSIONS)
def test_verify_binary(extension, monkeypatch):
    monkeypatch.setattr("pytest_approval.main.REPORTERS_BINARY", [REPORTERS_BINARY[1]])
    with open(FIXTURE_DIR / f"binary{extension}", "rb") as file:
        data = file.read()

    assert verify_binary(data, extension=extension)


def test_verify_gnu_diff_tools_approver(monkeypatch):
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", [REPORTERS_TEXT[-1]])
    with pytest.raises(AssertionError) as error:
        assert verify("Hello World!")
    expected = r"""Received is different from approved.
To approve run mv --force /home/matthias/projects/pytest-approval/tests/test_main.py--test_verify_gnu_diff_tools_approver.received.txt /home/matthias/projects/pytest-approval/tests/test_main.py--test_verify_gnu_diff_tools_approver.approved.txt
--- received
+++ approved
@@ -1 +0,0 @@
-Hello World!
"""  # noqa
    assert expected == str(error.value)


def test_verify_approved_equal(approved, fake_process):
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is True
    assert fake_process.call_count(["meld", fake_process.any()]) == 0


def test_verify_approved_different(approved_different, fake_process):
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is False
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


def test_verify_approved_none(fake_process):
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is False
    assert fake_process.call_count(["meld", fake_process.any()]) == 1


def test_verify_different_returncode_127(fake_process, caplog):
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
