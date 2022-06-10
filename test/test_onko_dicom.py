"""
Tests for onko_dicom.py
"""
import pytest
from src.onko_dicom import OnkoDicom


@pytest.fixture
def test_app(qtbot):
    """
    Sets up application for testing
    """
    test_app = OnkoDicom()
    qtbot.addWidget(test_app)
    return test_app


def test_startup(test_app):
    """Tests window startup, ensuring it runs"""
    assert test_app.windowTitle() == "OnkoDICOM 2022 Mini Project"
    assert test_app.plot_w


def test_close_event(qtbot, test_app):
    """Tests close event of window"""
    with qtbot.waitSignal(test_app.closeEvent(), raising=True):
        test_app.exec()
