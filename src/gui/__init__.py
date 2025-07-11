import sys

from PySide6 import QtCore, QtWidgets

from ..player import Player
from .controls import ControlsWidget
from .playlist import PlaylistWidget
from .song_info import SongInfoWidget

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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)

        self.playlist = PlaylistWidget(self, self.player)
        main_layout.addWidget(self.playlist)

        self.song_info = SongInfoWidget(self, self.player)
        main_layout.addWidget(self.song_info)

        self.controls = ControlsWidget(self, self.player)
        main_layout.addWidget(self.controls)

        # Periodic update of the UI

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(UPDATE_DELAY)

    def update_ui(self) -> None:
        self.playlist.update_ui()
        self.song_info.update_ui()
        self.controls.update_ui()

    def __del__(self):
        self.player.quit()
