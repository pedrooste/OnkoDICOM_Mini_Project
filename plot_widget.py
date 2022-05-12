"""
Integrates pydicom, matplotlib and PySide6 together
"""

import logging
import sys

import matplotlib.axes
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logs/plot_widget.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class PlotWidget(QWidget):
    """
    Creates a custom QWidget, used for displaying a dcm file in other QtWidgets
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Initialising PlotWidget")

        #  Create widgets
        self.view = FigureCanvasQTAgg(Figure(figsize=(5, 5)))
        self.axes = self.view.figure.subplots()
        self.axes.axis('off')  # same as set_axis_off()

        #  Create layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.view)
        self.setLayout(vertical_layout)

        logger.info("Initialising PlotWidget complete")

    def plot_dcm(self, path):
        """
        Plots the dcm file in the axes and view
        """
        logger.info("plot_dcm started within PlotWidget")

        data_source = pydicom.dcmread(path)
        self.axes.clear()
        self.axes.imshow(data_source.pixel_array, cmap=plt.cm.bone)
        self.axes.set_title(path.rsplit('/', 1)[1])
        self.view.draw()

        logger.info("plot_dcm completed within PlotWidget")
        return self.axes.axis() != (0.0, 1.0, 0.0, 1.0)

    def clear_view(self):
        """
        Clears the axes and view
        """
        logger.info("clear_view started within PlotWidget")

        self.axes.clear()
        self.axes.axis('off')
        self.view.draw()

        logger.info("clear_view completed within PlotWidget")
        return self.axes.axis() == (0.0, 1.0, 0.0, 1.0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(app.exec())
