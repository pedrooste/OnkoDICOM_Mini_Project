"""Data model to store all file paths"""
from PySide6 import QtCore


class PathsModel(QtCore.QStringListModel):
    """Contains all of the Paths inside a QStringList"""

    def __init__(self, paths=None):
        super().__init__()
        self.paths = paths or []

    def path_count(self):
        """returns the amount of paths stored"""
        return len(self.paths)
