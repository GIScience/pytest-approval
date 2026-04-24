import os

import plotly.graph_objects as go
import pytest
from pytest_nodeid_to_filepath import get_filepath

from pytest_approval import verify, verify_plotly
from pytest_approval.definitions import REPORTERS

FIG = go.Figure(
    data=go.Contour(
        z=[
            [10, 10.625, 12.5, 15.625, 20],
            [5.625, 6.25, 8.125, 11.25, 15.625],
            [2.5, 3.125, 5.0, 8.125, 12.5],
            [0.625, 1.25, 3.125, 6.25, 10.625],
            [0, 0.625, 2.5, 5.625, 10],
        ]
    )
)


@pytest.mark.parametrize(
    "figure",
    (
        FIG,
        FIG.to_dict(),
        FIG.to_json(),
        FIG.to_plotly_json(),
    ),
)
def test_verify_plotly(figure):
    assert verify_plotly(figure)


@pytest.mark.skipif(
    os.environ.get("CI", None) is not None,
    reason="In CI environ Plotly can not export an image.",
)
def test_verify_plotly_report_always(fake_process):
    fake_process.register_subprocess(["pycharm", fake_process.any()])
    fake_process.allow_unregistered(True)
    assert not verify_plotly(FIG, report_always=True)
    assert fake_process.call_count(["pycharm", fake_process.any()]) == 1


@pytest.mark.skipif(
    os.environ.get("CI", None) is None,
    reason="In PC environ Plotly can export an image.",
)
def test_verify_plotly_report_always_2():
    # Same as above test but this time expect verification to be successful
    assert verify_plotly(FIG, report_always=True)


def test_verify_plotly_not_approved(monkeypatch: pytest.MonkeyPatch):
    # Are the all files (.json and .png) removed even if no approval was given?
    monkeypatch.setattr("pytest_approval.main.REPORTERS", {"diff": REPORTERS["diff"]})
    filepath = get_filepath(directory="tests/approvals", count=False)

    verify_plotly(FIG)

    assert not filepath.with_suffix(filepath.suffix + ".approved.png").exists()
    assert not filepath.with_suffix(filepath.suffix + ".received.png").exists()

    assert not filepath.with_suffix(filepath.suffix + ".approved.json").exists()
    assert filepath.with_suffix(filepath.suffix + ".received.json").exists()


def test_verify_plotly_two_calls_to_verify(monkeypatch):
    # This covers a bug where the second image written to disk has not been removed
    monkeypatch.setattr("pytest_approval.main.REPORTERS", {"diff": REPORTERS["diff"]})
    filepath = get_filepath(directory="tests/approvals", count=False)

    verify("foo")
    verify_plotly(FIG)

    assert not filepath.with_suffix(filepath.suffix + ".approved.txt").exists()
    assert filepath.with_suffix(filepath.suffix + ".received.txt").exists()

    assert not filepath.with_suffix(filepath.suffix + ".approved.png").exists()
    assert not filepath.with_suffix(filepath.suffix + ".received.png").exists()

    assert not filepath.with_suffix(filepath.suffix + ".approved.json").exists()
    assert filepath.with_suffix(filepath.suffix + ".received.json").exists()
