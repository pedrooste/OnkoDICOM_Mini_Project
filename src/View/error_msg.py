"""Generic error message to be displayed"""
from PySide6.QtWidgets import QMessageBox, QWidget





class ErrorMessage(QWidget):
    """Generic Err message class"""

    def __init__(self, title, msg):
        super().__init__()
        self.msg_box = QMessageBox(QMessageBox.Icon.Critical, title, msg)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setText(msg)
        self.msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        self.force_button = self.msg_box.button(QMessageBox.Yes)
        self.force_button.setText('Force Open')

        self.close_button = self.msg_box.button(QMessageBox.No)
        self.close_button.setText('Abort')

        self.response = self.msg_box.exec()

        if self.response == self.force_button:
            self.force_open()
        else:
            self.close_msg()

    def force_open(self):
        """Returns true to force open"""
        return True

    def close_msg(self):
        """Returns false to close err msg"""
        return False
