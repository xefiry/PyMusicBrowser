import sys

from PySide6 import QtCore, QtWidgets

from ..player import Player
from .controls import ControlsWidget
from .playlist import PlaylistWidget

UPDATE_DELAY = 100  # 0.1 s


def start() -> None:
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    rv = app.exec()

    sys.exit(rv)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.player = Player()

        # UI building

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.playlist = PlaylistWidget(self)
        main_layout.addWidget(self.playlist)

        self.controls = ControlsWidget(self, self.player)
        main_layout.addWidget(self.controls)

        # Controls connection

        self.current_song = -1

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(UPDATE_DELAY)

        self.update_ui()

    def update_ui(self) -> None:
        self.controls.update_ui()

        song_list = self.player.get_song_list()
        if self.current_song != song_list[1]:
            print("updating playlist")
            self.playlist.set_list(song_list)
            self.current_song = song_list[1]

    def __del__(self):
        self.player.quit()
