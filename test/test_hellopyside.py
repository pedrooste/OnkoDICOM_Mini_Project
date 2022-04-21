"""Testing file for hellopyside file"""
import pytest
from PySide6 import QtCore
import hellopyside


@pytest.fixture
def test_app(qtbot):
    """sets up application for testing"""
    app = hellopyside.OnkoDicom()
    qtbot.addWidget(app)

    return app


def test_startup(app):
    """Tests window startup, ensuring it runs"""
    assert app.text_label.text() == "Doubled: "
    assert app.input_double.placeholderText() == "Enter a text to double"


def test_double(app, qtbot):
    """Tests button functionality"""
    qtbot.keyClicks(app.input_double, 'abc')
    qtbot.mouseClick(app.button_double, QtCore.Qt.LeftButton)
    assert app.text_label.text() == "Doubled: abcabc"
    assert app.input_double.text() == "abcabc"
