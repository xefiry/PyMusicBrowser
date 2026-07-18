import sys

from PySide6 import QtWidgets

from .main_window import MainWindow

# TODO Add tray icon
# TODO Add mini player
# TODO Handle multi CD albums
# TODO Show notification on song change if window is not visible
# TODO test other themes (check [qt-themes](https://github.com/beatreichenbach/qt-themes))


def start() -> None:
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    rv = app.exec()

    sys.exit(rv)
