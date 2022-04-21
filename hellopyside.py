""" This file starts up the QT hello world window with some basic functionality"""
import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

logging.basicConfig(
    filename='hellopyside.log',
    level=logging.DEBUG,
    format='%(levelname)s:%(message)s', force=True
)


class OnkoDicom(QtWidgets.QWidget):
    """ Encapsulates and sets main window """

    def __init__(self):
        super().__init__()

        self.text_label = QtWidgets.QLabel("Doubled: ")
        self.text_label.setAlignment(Qt.AlignCenter)

        self.input_double = QtWidgets.QLineEdit()
        self.input_double.setPlaceholderText("Enter a text to double")

        self.button_double = QPushButton("Double text")
        self.button_double.clicked.connect(self.double_text)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.input_double)
        self.layout.addWidget(self.button_double)

    def double_text(self):
        """ double input and set label"""
        text_double = self.input_double.text() * 2
        logging.info("Doubled -> " + text_double)
        self.input_double.setText(text_double)
        self.text_label.setText("Doubled: " + text_double)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = OnkoDicom()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
