"""Testing file for hellopyside file"""
import pytest
from PySide6 import QtCore
import hellopyside


@pytest.fixture
def test_app(qtbot):
    """sets up application for testing"""
    test_app = hellopyside.OnkoDicom()
    qtbot.addWidget(test_app)

    return test_app


def test_startup(test_app):
    """Tests window startup, ensuring it runs"""
    assert test_app.main_window.text_heading.text() == "OnkoDICOM 2022 Mini Project"
    assert test_app.main_window.text_label.text() == "Doubled: "
    assert test_app.main_window.input_double.placeholderText() == "Enter a text to double"


def test_double(test_app, qtbot):
    """Tests button functionality"""
    qtbot.keyClicks(test_app.main_window.input_double, 'abc')
    qtbot.mouseClick(test_app.main_window.button_double, QtCore.Qt.LeftButton)
    assert test_app.main_window.text_label.text() == "Doubled: abcabc"
    assert test_app.main_window.input_double.text() == "abcabc"

def test_import(test_app, qtbot):
    """Tests import button on menubar"""
    # not too sure
