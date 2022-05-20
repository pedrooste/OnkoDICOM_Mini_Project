"""
Integrates pydicom, matplotlib and PySide6 together
"""

import logging
import os
import pydicom
import pydicom.data
from PySide6.QtCore import Qt
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSlider
)

LOG_FILES_DIR = 'logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

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
        self.slider = QSlider(Qt.Horizontal)

        #  Create layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.view)
        vertical_layout.addWidget(self.slider)
        self.setLayout(vertical_layout)

        # Disable slider
        self.slider.setEnabled(False)

        # Default min and max
        self.slider.setMinimum(1)
        self.slider.setMaximum(1)

        # Connect slider
        self.slider.valueChanged.connect(self.update_plot)

        # Paths var
        self.paths = None

        logger.info("Initialising PlotWidget complete")

    def update_plot(self, value):
        """
        Updates the plot whenever the slider's value is changed
        """
        return self.plot_dcm(value)

    def set_paths(self, paths):
        """
        Set the paths of the dcm files in the parsed dir
        """
        logger.info("set_paths started within PlotWidget")
        self.paths = paths

        # Parse 1 to plot the first dcm file
        self.plot_dcm(1)

        # Update slider
        self.slider.setEnabled(True)
        self.slider.setMaximum(len(self.paths))

        logger.info("set_paths completed within PlotWidget")

        return bool(self.paths)

    def plot_dcm(self, value):
        """
        Plots the dcm file in the axes and view
        """
        logger.info("plot_dcm started within PlotWidget")

        path = self.paths[value-1]

        try:
            logger.info("Attempting to graph/open file (%s)", path)
            data_source = pydicom.dcmread(path)
            self.axes.clear()
            self.axes.imshow(data_source.pixel_array, cmap=plt.cm.bone)
            self.axes.set_title(path.rsplit('/', 1)[1])
            self.view.draw()

            logger.info("plot_dcm completed within PlotWidget")
            return self.axes.axis() != (0.0, 1.0, 0.0, 1.0)
            logger.info("successfully opened graph/file (%s)", path)

        except pydicom.errors.InvalidDicomError as err:
            logger.error("(%s): InvalidDicomError, Missing Dicom Header. Error:(%s)", path, err)
        except AttributeError as err:
            logger.error("(%s): AttributeError, Missing Attribute. Error:(%s)", path, err)
        except Exception as err:
            logger.error("(%s): Error:(%s)", path, err)

    def force_plot_dcm(self, path):
        """
        Force plots the dcm file in the axes and view
        """
        logger.info("force_plot_dcm started within PlotWidget")

        data_source = pydicom.dcmread(path, force=True)
        if "TransferSyntaxUID" not in data_source.file_meta:
            data_source.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
            # pydicom.write_file(path, data_source)
        self.axes.clear()
        self.axes.imshow(data_source.pixel_array, cmap=plt.cm.bone)
        self.axes.set_title(path.rsplit('/', 1)[1])
        self.view.draw()

        logger.info("force_plot_dcm completed within PlotWidget")
        return self.axes.axis() != (0.0, 1.0, 0.0, 1.0)

    def clear_view(self):
        """
        Clears the axes and view
        """
        logger.info("clear_view started within PlotWidget")

        self.slider.setEnabled(False)
        self.slider.setValue(1)
        self.axes.clear()
        self.axes.axis('off')
        self.view.draw()

        logger.info("clear_view completed within PlotWidget")
        return self.axes.axis() == (0.0, 1.0, 0.0, 1.0)
