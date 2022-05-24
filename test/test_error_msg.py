"""
Tests for plot_widget.py
"""
import pytest
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox

from src.View.error_msg import ErrorMessage


@pytest.fixture
def test_app(qtbot):
    """
    Sets up widget for testing
    """
    test_app = ErrorMessage('Title', 'Message')
    qtbot.addWidget(test_app)
    return test_app


def test_check_content(test_app, qtbot):
    """Checks content within the msg box"""
    assert test_app.msg_box.icon() == QMessageBox.Icon.Critical
    assert test_app.msg_box.windowTitle() == 'Title'
    assert test_app.msg_box.text() == 'Message'

    qtbot.mouseClick(test_app.close_button, QtCore.Qt.LeftButton, delay=1)
