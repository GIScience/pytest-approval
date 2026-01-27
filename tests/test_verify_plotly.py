import os
from pathlib import Path

import plotly.graph_objects as go
import pytest

from pytest_approval import verify_plotly
from pytest_approval.definitions import REPORTERS
from pytest_approval.main import NAMES_WITHOUT_EXTENSION, _name

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


def test_verify_ploty_not_approved(monkeypatch):
    # Are the all files (.json and .png) removed even if no approval was given?
    monkeypatch.setattr("pytest_approval.main.REPORTERS", {"diff": REPORTERS["diff"]})
    assert not verify_plotly(FIG)
    NAMES_WITHOUT_EXTENSION.pop()
    received, approved = _name()
    approved = Path(str(approved).replace(".txt", ".json"))
    received = Path(str(received).replace(".txt", ".json"))
    assert not approved.exists()
    received.unlink()
