"""
This file starts up the QMainWindow with a custom QtWidget, plot_widget
"""

import logging
import os
import sys
import pydicom

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog
)
import plot_widget
from resources.settings import load_settings


LOG_FILES_DIR = 'logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logs/onko_dicom.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class OnkoDicom(QMainWindow):
    """
    Encapsulates and sets main window
    """
    def __init__(self):
        super().__init__()
        logger.info("Initialising OnkoDicom")

        self.close_action = None
        self.open_action = None
        self.resize(settings.window_x, settings.window_y)
        self.show()

        self.setWindowTitle("OnkoDICOM 2022 Mini Project")
        self.create_menu()

        self.plot_w = plot_widget.PlotWidget()
        self.setCentralWidget(self.plot_w)

        logger.info("Initialising OnkoDicom completed")

    def create_menu(self):
        """Menu bar displayed at the top of the page"""
        logger.info("Initialising Menu within OnkoDicom")

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")

        self.open_action = QAction("Open DICOM File", self)
        self.open_action.triggered.connect(lambda: self.open_file())

        self.close_action = QAction("Close File", self)
        self.close_action.triggered.connect(lambda: self.close_file())
        self.close_action.setEnabled(False)

        file_menu.addAction(self.open_action)
        file_menu.addAction(self.close_action)

        logger.info("Initialised Menu within OnkoDicom")

    def open_file(self):
        """Opens a file import window"""
        logger.info("open_file started within OnkoDicom")

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
            logger.info("open_file user canceled open operation")
            return

        try:
            logger.info("Attempting to graph/open file (%s)", full_path[0])
            self.plot_w.plot_dcm(full_path[0])
            self.close_action.setEnabled(True)
            logger.info("successfully opened graph/file (%s)", full_path[0])

        except pydicom.errors.InvalidDicomError as err:
            logger.error("(%s): InvalidDicomError, Missing Dicom Header. Error:(%s)", full_path[0], err)
        except AttributeError as err:
            logger.error("(%s): AttributeError, Missing Attribute. Error:(%s)", full_path[0], err)
        except Exception as err:
            logger.error("(%s): Error:(%s)", full_path[0], err)


    def close_file(self):
        """Clears the file from the view"""
        logger.info("close_file started within OnkoDicom")

        self.plot_w.clear_view()
        self.close_action.setEnabled(False)

        logger.info("close_file completed within OnkoDicom")


if __name__ == "__main__":
    settings = load_settings(1)

    app = QtWidgets.QApplication([])
    OnkoDicom()
    sys.exit(app.exec())
