# pylint: disable=no-member
"""
Integrates pydicom, matplotlib and PySide6 together
"""

import sys
import glob
import pydicom
import pydicom.data
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)


class PlotWidget(QWidget):
    """
    Creates a GUI window
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        #  Create widgets
        self.view = FigureCanvasQTAgg(Figure(figsize=(5, 5)))
        self.axes = self.view.figure.subplots()
        self.axes.axis('off')
        self.button = QPushButton("Select")
        self.input = QSpinBox()

        #  Create layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.button)
        input_layout.addWidget(self.input)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.view)
        vertical_layout.addLayout(input_layout)
        self.setLayout(vertical_layout)

        # Connect button with on_click method
        self.button.clicked.connect(self.on_click)

        # Set min and max values for q_spin_box
        self.input.setMinimum(1)
        self.input.setMaximum(len(PATHS))

    @Slot()
    def on_click(self):
        """
        Updates the axes and view in the GUI
        """
        path = PATHS[self.input.value() - 1]
        data_source = pydicom.dcmread(path)
        self.axes.clear()
        self.axes.imshow(data_source.pixel_array, cmap=plt.cm.bone)
        self.axes.set_title(path.rsplit('\\', 1)[1])
        self.view.draw()


PATHS = None
if __name__ == "__main__":
    # The dir where the dcm files are stored
    PATHS = glob.glob(r"E:\CSIT321\OnkoDICOM_Mini_Project\dcm\*.dcm")

    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(app.exec())
