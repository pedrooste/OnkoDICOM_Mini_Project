"""Generic error message to be displayed"""
from PySide6.QtWidgets import QMessageBox, QWidget
import logging
import os
LOG_FILES_DIR = '../logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('../logs/menu_bar.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ErrorMessage(QWidget):
    """Generic Err message class"""

    def __init__(self, title, msg):
        logger.info("Initialising error message")
        super().__init__()
        self.msg_box = QMessageBox(QMessageBox.Icon.Critical, title, msg)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setText(msg)
        self.msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        self.force_button = self.msg_box.button(QMessageBox.Yes)
        self.force_button.setText('Force Open')

        self.close_button = self.msg_box.button(QMessageBox.No)
        self.close_button.setText('Abort')
        logger.info("Error message initialised")

    def get_response(self):
        """Checks err msg button that the user has clicked"""
        logger.info("Checking error message button user pressed")
        response = self.msg_box.exec()

        if response == QMessageBox.Yes:
            logger.info("Pressed True")
            return True
        else:
            logger.info("Pressed False")
            return False

