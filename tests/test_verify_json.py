import pytest

from pytest_approval import scrub, verify_json


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


def test_verify_json_scrub():
    d = "2021-01-01T00:00:00+00:00"
    j = {"date": d}
    scrub_datetime = scrub.get_datetime_scrubber(d)
    assert verify_json(j, sort=True, scrub=scrub_datetime)
