"""
Tests for plot_widget.py
"""
import glob
import pytest
from src.View.plot_widget import PlotWidget


@pytest.fixture
def test_app(qtbot):
    """
    Sets up widget for testing
    """
    test_app = PlotWidget()
    qtbot.addWidget(test_app)
    return test_app


def test_update_plot(test_app):
    """
    Tests plot_widget update_plot function
    """
    assert test_app.set_paths(glob.glob(r"test/test files/DICOM-RT-01/*.dcm"))
    assert test_app.update_plot(2)


def test_set_paths(test_app):
    """
    Tests plot_widget set_paths function
    """
    assert test_app.set_paths(glob.glob(r"test/test files/DICOM-RT-01/*.dcm"))


def test_plot_dcm(test_app):
    """
    Tests plot_widget plot_dcm function
    """
    assert test_app.set_paths(glob.glob(r"test/test files/DICOM-RT-01/*.dcm"))
    assert test_app.plot_dcm(2)


def test_clear_view(test_app):
    """
    Tests plot_widget clear_view function
    """
    assert test_app.clear_view()
