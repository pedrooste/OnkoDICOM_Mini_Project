"""
Tests for err_msg.py
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
    test_app = ErrorMessage(title='Title', msg='Message')
    qtbot.addWidget(test_app)
    return test_app


def test_check_content(test_app, qtbot):
    """Checks content within the msg box"""
    assert test_app.msg_box.icon() == QMessageBox.Icon.Critical
    assert test_app.msg_box.windowTitle() == 'Title'
    assert test_app.msg_box.text() == 'Message'


def test_close(test_app, qtbot):
    assert test_app

    button = test_app.close_button
    QtCore.QTimer.singleShot(0, button.clicked)
    test_app.get_response()
