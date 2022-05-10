import sys
from PySide6 import QtCore, QtWidgets
import sqliteconnection

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)


    example_settings_table = """CREATE TABLE IF NOT EXISTS SETTINGS (
                                    id integer PRIMARY KEY,
                                    setting text NOT NULL,
                                    state integer NOT NULL
                                );"""

    # Testing database connection
    connection = sqliteconnection.connect("pythonsqlite.db")

    if connection is not None:
        sqliteconnection.construct_table(connection, example_settings_table)

    else:
        print("Error failed to connect to database")

    #test = (1, "Test Setting", 1)

    #sqliteconnection.create_task(connection, test) #state == 1 == true

    widget.show()

    sys.exit(app.exec())