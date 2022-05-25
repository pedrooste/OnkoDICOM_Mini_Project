"""
Tests for plot_widget.py
"""
import time

import pytest
from PySide6 import QtCore, QtWidgets, QtTest, QtGui
from PySide6.QtTest import QTest
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
    # qtbot.mouseClick(test_app.close_button, QtCore.Qt.LeftButton, delay=1)
    # QTest.mouseClick(test_app.close_button, QtCore.Qt.LeftButton)
    # print(type(test_app.close_button))

    assert test_app.msg_box.icon() == QMessageBox.Icon.Critical
    assert test_app.msg_box.windowTitle() == 'Title'
    assert test_app.msg_box.text() == 'Message'
