"""
This file starts up the QMainWindow with a custom QtWidget, plot_widget
"""

import logging
import os
import sys
import glob

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox
)
import plot_widget
from resources.settings import load_settings
import pydicom

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

        self.open_action = QAction("Open Directory", self)
        self.open_action.triggered.connect(lambda: self.open_dir())

        self.close_action = QAction("Close", self)
        self.close_action.triggered.connect(lambda: self.close_file())
        self.close_action.setEnabled(False)

        file_menu.addAction(self.open_action)
        file_menu.addAction(self.close_action)

        logger.info("Initialised Menu within OnkoDicom")

    def err_msg(self, title, msg):
        """Error handling messagebox"""
        msg_box = QMessageBox(self, title, msg)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button_y = msg_box.button(QMessageBox.Yes)
        button_y.setText('Force Open')
        button_n = msg_box.button(QMessageBox.No)
        button_n.setText('Abort')
        msg_box.exec()

        if msg_box.clickedButton() == button_y:
            return 'F'
        elif msg_box.clickedButton() == button_n:
            return 'A'

    def open_dir(self):
        """Opens a file import window"""
        logger.info("open_dir started within OnkoDicom")

        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        files = os.path.join(directory, "*.dcm").replace("\\", "/")
        paths = sorted(glob.glob(files))

        # If user cancels open, path is empty
        if not paths:
            logger.info("open_dir user canceled open operation")
            return

        """Error handling"""
        self.plot_w.set_paths(paths)
        self.close_action.setEnabled(True)
        try:
            logger.info("Attempting to graph/open file (%s)", full_path[0])
            self.plot_w.plot_dcm(full_path[0])
            self.close_action.setEnabled(True)
            logger.info("successfully opened graph/file (%s)", full_path[0])

        except pydicom.errors.InvalidDicomError as err:
            logger.error("(%s): InvalidDicomError, Missing Dicom Header. Error:(%s)", full_path[0], err)
            response = self.err_msg('Error', 'InvalidDicomError, Missing Dicom Header. \n\nError: '
                                    + '<br>'.join([str(err)]))
            if response == 'F':
                self.plot_w.force_plot_dcm(full_path[0])
                self.close_action.setEnabled(True)
                logger.info("successfully force opened graph/file (%s)", full_path[0])
            else:
                pass

        except AttributeError as err:
            logger.error("(%s): AttributeError, Missing Attribute. Error:(%s)", full_path[0], err)
            response = self.err_msg('Error', 'AttributeError, Missing Attribute. \n\nError: ' + '<br>'.join([str(err)]))
            if response == 'F':
                self.plot_w.force_plot_dcm(full_path[0])
                self.close_action.setEnabled(True)
                logger.info("successfully force opened graph/file (%s)", full_path[0])
            else:
                pass

        except NotImplementedError as err:
            try:
                logger.error("(%s): NotImplementedError. Error:(%s)", full_path[0], err)
                self.err_msg('Error', 'NotImplementedError. \n\nError: ' + ''.join([str(err)]))
            except ValueError as err:
                logger.error("(%s): ValueError. Error:(%s)", full_path[0], err)
                response = self.err_msg('Error', 'NotImplementedError and ValueError. \n\nError: ' +
                                        "Unable to decode pixel data  with a transfer syntax UID"
                                        "as there are no pixel data handlers "
                                        "available that support it. Please see the pydicom "
                                        "documentation for information on supported transfer syntaxes\n\n"
                                        + 'Error: ' + ''.join([str(err)])
                                        )
                if response == 'F':
                    import webbrowser
                    webbrowser.open('https://pydicom.github.io/pydicom/stable/old/image_data_handlers.html',
                                    new=0, autoraise=True)
                    logger.info("Open pydicom document")

        except Exception as err:
            logger.error("(%s): Error:(%s)", full_path[0], err)
            self.err_msg('Error', 'Error: ' + ''.join([str(err)]))

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
