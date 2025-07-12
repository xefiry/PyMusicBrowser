import sys

from PySide6 import QtCore, QtWidgets

from ..player import Player
from .browser import BrowserWidget
from .controls import ControlsWidget
from .navigation import NavigationWidget
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

        # UI content

        self.playlist = PlaylistWidget(self, self.player)
        self.song_info = SongInfoWidget(self, self.player)
        self.navigator = NavigationWidget(self, self.player)
        self.browser = BrowserWidget(self, self.player)
        self.controls = ControlsWidget(self, self.player)

        # UI building => Side = Playlist + Song info

        side_widget = QtWidgets.QWidget()
        side_widget.setFixedWidth(300)

        side_layout = QtWidgets.QVBoxLayout()
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)
        side_widget.setLayout(side_layout)

        side_layout.addWidget(self.playlist)
        side_layout.addWidget(self.song_info)

        # UI building => Top = Navigator + Browser + Side

        top_widget = QtWidgets.QWidget()

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        top_widget.setLayout(top_layout)

        top_layout.addWidget(self.navigator)
        top_layout.addWidget(self.browser)
        top_layout.addWidget(side_widget)

        # UI building => Main = Top + Controls

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)

        main_layout.addWidget(top_widget)
        main_layout.addWidget(self.controls)

        # Periodic update of the UI

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(UPDATE_DELAY)

    def update_ui(self) -> None:
        self.playlist.update_ui()
        self.song_info.update_ui()
        self.navigator.update_ui()
        self.browser.update_ui()
        self.controls.update_ui()

    def __del__(self):
        self.player.quit()
