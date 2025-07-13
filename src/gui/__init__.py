import sys

from PySide6 import QtWidgets

from .main_window import MainWindow


def start() -> None:
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    rv = app.exec()

    sys.exit(rv)
