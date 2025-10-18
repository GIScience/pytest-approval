import pytest

from pytest_approval import verify_json


@pytest.mark.parametrize(
    "json",
    (
        {"b": 100, "a": None},
        '{"b": 100, "a": null}',
        [100, "a", None],
    ),
)
def test_verify_json(json):
    assert verify_json(json)


@pytest.mark.parametrize(
    "json",
    (
        {"b": 100, "a": {"d": 10, "c": 10}},
        [100, 1],
        ["b", "a"],
    ),
)
def test_verify_json_sort(json):
    assert verify_json(json, sort=True)
