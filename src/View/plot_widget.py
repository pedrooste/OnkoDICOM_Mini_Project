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
    QSlider,
    QMessageBox
)

from src.Model.paths_model import PathsModel
from src.View.error_msg import ErrorMessage

LOG_FILES_DIR = '../../logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('../../logs/plot_widget.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

allDCM = []

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

        # Paths model
        self.paths_model = PathsModel()

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
        self.paths_model.paths.clear()
        self.paths_model.paths.extend(paths)


        #load all files
        for path in paths:
            allDCM.append(pydicom.dcmread(path))

        allDCM.sort(key=lambda ds: float(ds.get_item((0x0020, 0x1041)).value), reverse=True)

        # Parse 1 to plot the first dcm file
        test = self.plot_dcm(1)
        print("test: " + str(test))
        # Update slider
        self.slider.setEnabled(True)
        self.slider.setMaximum(self.paths_model.path_count())

        logger.info("set_paths completed within PlotWidget")

        return bool(self.paths_model)

    def plot_dcm(self, value, data_source=None):
        data_source = allDCM[value - 1]
        """
        Plots the dcm file in the axes and view
        """
        logger.info("plot_dcm started within PlotWidget")

        path = self.paths_model.paths[value - 1]

        try:
            logger.info("Attempting to graph/open file (%s)", path)
            return self.open_dicom_file(path, False, data_source)

        except pydicom.errors.InvalidDicomError as err:
            response = self.display_err_msg("Error", 'InvalidDicomError, Missing Dicom Header. \n\nError: '
                                            + '<br>'.join([str(err)]))
            if response:
                logger.info("force_plot_dcm started within PlotWidget")
            self.open_dicom_file(path, True)

            self.display_dialog()

        except NotImplementedError as err:
            logger.info(
                "Error, see related information https://pydicom.github.io/pydicom/stable/old/image_data_handlers.html")

        except (AttributeError, Exception) as err:
            logger.error("(%s): Error:(%s)", path, err)
            self.display_dialog()

    def display_err_msg(self, title, err):
        """Renders Error message"""
        return ErrorMessage(self, title, err).get_response()

    def display_dialog(self, title="Error", msg="Unable to open this dcm file"):
        """Renders dialog prompt"""
        msg = QMessageBox(QMessageBox.Icon.Critical, title, msg, parent=self)
        msg.exec()
        logger.info("Unable to open graph/file")

    def open_dicom_file(self, path, force, data_source=None):
        """Opens dicom file"""
        logger.info("Attempting to graph/open file (%s)", path)
        if data_source is None:
            data_source = pydicom.dcmread(path, force=force)

        if "TransferSyntaxUID" not in data_source.file_meta and force:
            data_source.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
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

        self.slider.setEnabled(False)
        self.slider.setValue(1)
        self.axes.clear()
        self.axes.axis('off')
        self.view.draw()

        logger.info("clear_view completed within PlotWidget")
        return self.axes.axis() == (0.0, 1.0, 0.0, 1.0)
