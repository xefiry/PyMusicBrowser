import sys

from controls import ControlsWidget
from PySide6 import QtWidgets


def start() -> None:
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    rv = app.exec()

    sys.exit(rv)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.controls = ControlsWidget(self)

        self.setCentralWidget(self.controls)


start()
