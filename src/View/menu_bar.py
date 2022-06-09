"""menu bar for main Onko_dicom window"""
import glob
import logging
import os

from IPython.external.qt_for_kernel import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog

LOG_FILES_DIR = '../logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('../logs/menu_bar.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MenuBar(QtWidgets.QMenuBar):
    """Menu bar displayed at the top of the page"""

    def __init__(self, onko_dicom):
        QtWidgets.QMenuBar.__init__(self)
        self.onko_dicom = onko_dicom
        self.setGeometry(QtCore.QRect(0, 0, 901, 35))
        self.setContextMenuPolicy(Qt.PreventContextMenu)

        logger.info("Initialising Menu within OnkoDicom")

        self.file_menu = self.addMenu("File")

        self.open_action = QAction("Open Directory", self)
        self.open_action.triggered.connect(lambda: self.open_dir())

        self.close_action = QAction("Close", self)
        self.close_action.triggered.connect(lambda: self.close_file())
        self.close_action.setEnabled(False)

        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.close_action)

        logger.info("Initialised Menu within OnkoDicom")

    def open_dir(self):
        """Opens a file import window"""
        logger.info("open_dir started within OnkoDicom")

        if os.path.isdir(self.onko_dicom.settings.dicom_path) is False:
            self.onko_dicom.settings.dicom_path = ''

        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.onko_dicom.settings.dicom_path))
        files = os.path.join(directory, "*.dcm").replace("\\", "/")
        paths = sorted(glob.glob(files))

        # If user cancels open, path is empty
        if not paths:
            logger.info("open_dir user canceled open operation")
            return

        # Saves parent directory of the opened subdirectory to use as open dialog default
        self.onko_dicom.settings.dicom_path = os.path.split(directory)[0]

        self.onko_dicom.plot_w.set_paths(paths)
        self.close_action.setEnabled(True)

        logger.info("open_dir completed within OnkoDicom")

    def close_file(self):
        """Clears the file from the view"""
        logger.info("close_file started within OnkoDicom")

        self.onko_dicom.plot_w.clear_view()
        self.close_action.setEnabled(False)

        logger.info("close_file completed within OnkoDicom")
