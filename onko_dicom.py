"""
This file starts up the QT hello world window with some basic functionality
"""

import logging
import os
import sys
from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog
)
import plot_widget

logging.basicConfig(
    filename='hellopyside.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s:%(message)s',
    force=True
)


class OnkoDicom(QMainWindow):
    """
    Encapsulates and sets main window
    """
    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        self.show()

        self.setWindowTitle('OnkoDICOM 2022 Mini Project')
        self.create_menu()

        self.plot_w = plot_widget.PlotWidget()
        self.setCentralWidget(self.plot_w)

    def create_menu(self):
        """Menu bar displayed at the top of the page"""
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")

        open_action = QAction("Open DICOM File", self)
        open_action.triggered.connect(lambda: self.open_file())

        close_action = QAction("Close File", self)
        close_action.triggered.connect(lambda: self.close_file())

        file_menu.addAction(open_action)
        file_menu.addAction(close_action)

    def open_file(self):
        """Opens a file import window"""
        file_filter = 'Dicom File (*.dcm)'
        full_path = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a File',
            dir=os.getcwd(),
            filter=file_filter,
            selectedFilter='Dicom File (*.dcm)'
        )

        # If user cancels open, path is empty
        if not full_path[0]:
            return

        self.plot_w.plot_dcm(full_path[0])

    def close_file(self):
        """Clears the file from the view"""
        self.plot_w.clear_view()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    OnkoDicom()
    sys.exit(app.exec())
