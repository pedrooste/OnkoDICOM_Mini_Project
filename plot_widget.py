"""
Integrates pydicom, matplotlib and PySide6 together
"""

import logging
import os
import pydicom
import pydicom.data
import webbrowser
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

        except pydicom.errors.InvalidDicomError as err:
            logger.error("(%s): InvalidDicomError, Missing Dicom Header. Error:(%s)", path, err)
            response = self.err_msg('Error', 'InvalidDicomError, Missing Dicom Header. \n\nError: '
                                    + '<br>'.join([str(err)]))
            if response == 'F':
                logger.info("force_plot_dcm started within PlotWidget")
                data_source = pydicom.dcmread(path, force=True)
                if "TransferSyntaxUID" not in data_source.file_meta:
                    data_source.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
                    # pydicom.write_file(path, data_source)
                self.axes.clear()
                self.axes.imshow(data_source.pixel_array, cmap=plt.cm.bone)
                self.axes.set_title(path.rsplit('/', 1)[1])
                self.view.draw()

                logger.info("successfully force opened graph/file (%s)", path)
                return self.axes.axis() != (0.0, 1.0, 0.0, 1.0)
            else:
                logger.info("Unable to open graph/file (%s)")

        except AttributeError as err:
            logger.error("(%s): AttributeError, Missing Attribute. Error:(%s)", path, err)
            response = self.err_msg('Error', 'AttributeError, Missing Attribute. \n\nError: ' + '<br>'.join([str(err)]))
            if response == 'F':
                logger.info("Unable to open graph/file")
            else:
                logger.info("Unable to open graph/file")

        except NotImplementedError as err:
            try:
                logger.error("(%s): NotImplementedError. Error:(%s)", path, err)
                self.err_msg('Error', 'NotImplementedError. \n\nError: ' + ''.join([str(err)]))

            except ValueError as err:
                logger.error("(%s): ValueError. Error:(%s)", path, err)
                response = self.err_msg('Error', 'NotImplementedError and ValueError. \n\nError: ' +
                                        "Unable to decode pixel data  with a transfer syntax UID"
                                        "as there are no pixel data handlers "
                                        "available that support it. Please see the pydicom "
                                        "documentation for information on supported transfer syntaxes\n\n"
                                        + 'Error: ' + ''.join([str(err)])
                                        )
                if response == 'F':
                    webbrowser.open('https://pydicom.github.io/pydicom/stable/old/image_data_handlers.html',
                                    new=0, autoraise=True)
                    logger.info("Unable to open graph/file, open pydicom document")
                else:
                    logger.info("Unable to open graph/file")

        except Exception as err:
            logger.error("(%s): Error:(%s)", path, err)
            response = self.err_msg('Error', 'Error: ' + ''.join([str(err)]))
            if response == 'F':
                logger.info("Unable to open graph/file")
            else:
                logger.info("Unable to open graph/file")

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
