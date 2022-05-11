"""
Integrates pydicom, matplotlib and PySide6 together
"""

import sys
import pydicom
import pydicom.data
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
)


class PlotWidget(QWidget):
    """
    Creates a custom QWidget, used for displaying a dcm file in other QtWidgets
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        #  Create widgets
        self.view = FigureCanvasQTAgg(Figure(figsize=(5, 5)))
        self.axes = self.view.figure.subplots()
        self.axes.axis('off')

        #  Create layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.view)
        self.setLayout(vertical_layout)

    def plot_dcm(self, path):
        """
        Plots the dcm file in the axes and view
        """
        data_source = pydicom.dcmread(path)
        self.axes.clear()
        self.axes.imshow(data_source.pixel_array, cmap=plt.cm.bone)
        self.axes.set_title(path.rsplit('/', 1)[1])
        self.view.draw()

    def clear_view(self):
        """
        Clears the axes and view
        """
        self.axes.clear()
        self.axes.axis('off')
        self.view.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(app.exec())
