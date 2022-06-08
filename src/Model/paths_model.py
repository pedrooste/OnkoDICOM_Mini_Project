"""Data model to store all file paths"""
from PySide6 import QtCore
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('../logs/menu_bar.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class PathsModel(QtCore.QStringListModel):
    """Contains all of the Paths inside a QStringList"""

    def __init__(self, paths=None):
        logger.info("Initialising paths model")
        super().__init__()
        self.paths = paths or []

    def path_count(self):
        """returns the amount of paths stored"""
        logger.info("Returned amount of paths stored")
        return len(self.paths)
