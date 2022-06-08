"""
This file starts up the QMainWindow with a custom QtWidget, plot_widget
"""

import logging
import os
import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QMainWindow,
)
from src.View import plot_widget
from resources.settings import load_settings
from src.View.menu_bar import MenuBar

LOG_FILES_DIR = '../logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('../logs/onko_dicom.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class OnkoDicom(QMainWindow):
    """
    Encapsulates and sets main window
    """

    def __init__(self):
        super().__init__()
        logger.info("Initialising OnkoDicom")
        self.settings = load_settings(1)

        self.resize(self.settings.window_x, self.settings.window_y)
        self.show()

        self.setWindowTitle("OnkoDICOM 2022 Mini Project")

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.plot_w = plot_widget.PlotWidget()
        self.setCentralWidget(self.plot_w)

        logger.info("Initialising OnkoDicom completed")


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    OnkoDicom()
    sys.exit(app.exec())
