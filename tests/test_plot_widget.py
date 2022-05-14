"""
Tests for plot_widget.py
"""
import pytest
from plot_widget import PlotWidget


@pytest.fixture
def test_app(qtbot):
    """
    Sets up widget for testing
    """
    test_app = PlotWidget()
    qtbot.addWidget(test_app)

    return test_app


def test_plot_dcm(test_app):
    """
    Tests plot_widget test_plot_dcm function
    """
    assert test_app.plot_dcm("tests/test files/DICOM-RT-01/CT_3_Hashed.dcm")


def test_clear_view(test_app):
    """
    Tests plot_widget test_clear_view function
    """
    assert test_app.clear_view()
