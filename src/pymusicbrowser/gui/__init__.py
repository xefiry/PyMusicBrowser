import sys

from PySide6 import QtWidgets

from .main_window import MainWindow

# TODO Add mini player
# TODO test other themes (check [qt-themes](https://github.com/beatreichenbach/qt-themes))


def start() -> None:
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.hide()

    rv = app.exec()

    sys.exit(rv)
