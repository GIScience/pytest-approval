from pytest_approval.main import _verify


def test_verify_auto_approve(path):
    assert not path.exists()
    assert _verify("Hello World!", extension=".txt", auto_approve=True)
    assert path.exists()
