import logging
import re
from pathlib import Path

import pytest

from pytest_approval import verify, verify_binary, verify_json
from pytest_approval.definitions import (
    BINARY_EXTENSIONS,
    REPORTERS_BINARY,
    REPORTERS_TEXT,
)
from pytest_approval.main import _name, USED_FILES, cleaner

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
    received, approved = _name()
    with open(approved, "w") as file:
        file.write("hello world")
    yield approved


@pytest.fixture
def path(monkeypatch):
    monkeypatch.setattr("pytest_approval.main._count", lambda _: "")
    received, approved = _name()
    yield approved
    approved.unlink(missing_ok=True)

@pytest.fixture
def preserve_used_files():
    original = USED_FILES.copy()
    yield
    USED_FILES.clear()
    USED_FILES.extend(original)

@pytest.fixture
def cleaner_test_dir(tmp_path):
    # Create test directory with some files
    files = ["keep1.txt", "keep2.txt", "remove1.txt", "remove2.txt"]
    for fname in files:
        (tmp_path / fname).write_text(f"Content of {fname}")
    return tmp_path

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
    monkeypatch.setattr("pytest_approval.main.AUTO_APPROVE", False)
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", [REPORTERS_TEXT[-1]])
    with pytest.raises(AssertionError) as error:
        assert verify("Hello World!")
    monkeypatch.setattr("pytest_approval.main.REPORTERS_TEXT", REPORTERS_TEXT)
    pattern = r"/([^\s]+)pytest-approval/"
    replacement = "path/to/repo/pytest-approval/"
    error_string = re.sub(pattern, replacement, str(error.value))
    assert verify(error_string)


def test_verify_approved_equal(approved, fake_process):
    fake_process.register_subprocess(["meld", fake_process.any()])
    assert verify("Hello World!") is True
    assert fake_process.call_count(["meld", fake_process.any()]) == 0


def test_verify_approved_different(approved_different, fake_process, monkeypatch):
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

def test_cleaner_removes_unused_files(cleaner_test_dir, preserve_used_files):
    USED_FILES.clear()
    USED_FILES.extend([
        cleaner_test_dir / "keep1.txt",
        cleaner_test_dir / "keep2.txt"
    ])
    cleaner(cleaner_test_dir)

    assert sorted(f.name for f in cleaner_test_dir.iterdir()) == ["keep1.txt", "keep2.txt"]

