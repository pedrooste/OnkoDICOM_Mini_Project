""" This file starts up the QT hello world window with some basic functionality"""
import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import QPushButton, QGridLayout, QMainWindow, QFrame

logging.basicConfig(
    filename='hellopyside.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s:%(message)s', force=True
)


class OnkoDicom(QMainWindow):
    """ Encapsulates and sets main window """

    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.show()

        self.setWindowTitle('OnkoDICOM 2022 Mini Project')
        self.create_menu()

        self.main_window = MainPage()
        self.setCentralWidget(self.main_window)


    def create_menu(self):
        """Menu bar displayed at the top of the page"""
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")

        import_action = QAction("Import", self)
        import_action.triggered.connect(lambda: self.import_file())

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(lambda: self.close_application())

        file_menu.addAction(import_action)
        file_menu.addAction(exit_action)

    def close_application(self):
        """Closes the application when triggered"""
        logging.info("Application quit")
        app.quit()

    def import_file(self):
        """Opens a file import window"""
        logging.info("import_file has not been implemented")


class MainPage(QtWidgets.QWidget):
    """Main page to display"""

    def __init__(self):
        super().__init__()

        # font sizes
        self.heading = QFont("Times New Roman", 20)
        self.body = QFont("Times New Roman", 15)

        # widgets
        self.text_heading = QtWidgets.QLabel("OnkoDICOM 2022 Mini Project")
        self.text_heading.setAlignment(Qt.AlignCenter)
        self.text_heading.setFont(self.heading)

        self.text_label = QtWidgets.QLabel("Doubled: ")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFont(self.body)

        self.input_double = QtWidgets.QLineEdit()
        self.input_double.setPlaceholderText("Enter a text to double")

        self.button_double = QPushButton("Double text")
        self.button_double.clicked.connect(self.double_text)

        # layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.text_heading, 1, 0, 1, 0)
        self.layout.addWidget(self.button_double, 4, 0, 1, 0)
        self.layout.addWidget(self.text_label, 5, 0)
        self.layout.addWidget(self.input_double, 5, 1)

    def double_text(self):
        """ double input and set label"""
        text_double = self.input_double.text() * 2
        logging.info("Doubled: %s", text_double)
        self.input_double.setText(text_double)
        self.text_label.setText("Doubled: " + text_double)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    OnkoDicom()
    sys.exit(app.exec())

