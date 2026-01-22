from pytest_approval.main import _verify


def test_verify_auto_approve(path):
    assert not path.exists()
    assert _verify("Hello World!", extension=".txt", auto_approve=True)
    assert path.exists()


def test_verify_report_suppress(path):
    assert not path.exists()
    assert not _verify("Hello World!", extension=".txt", report_suppress=True)
    # Check if created empty file for reporting is deleted afterwards because its empty
    assert not path.exists()
