from io import BytesIO

from pytest_approval.main import _write


def test_write_binary_directory_exists(tmp_path):
    approved = tmp_path / "approved.png"
    received = tmp_path / "received.png"
    _write(BytesIO(b"foo").read(), approved, received)


def test_write_binary_directory_exists_not(tmp_path):
    approved = tmp_path / "foo" / "approved.png"
    received = tmp_path / "bar" / "received.png"
    _write(BytesIO(b"foo").read(), approved, received)


def test_write_text_directory_exists(tmp_path):
    approved = tmp_path / "approved.txt"
    received = tmp_path / "received.txt"
    _write("foo", approved, received)


def test_write_text_directory_exists_not(tmp_path):
    approved = tmp_path / "foo" / "approved.txt"
    received = tmp_path / "bar" / "received.txt"
    _write("foo", approved, received)
