from pynput import keyboard
from PySide6 import QtCore, QtGui, QtWidgets

from ..player import Player
from .browser import BrowserWidget
from .controls import ControlsWidget
from .navigation import NavigationWidget
from .playlist import PlaylistWidget
from .song_info import SongInfoWidget

UPDATE_DELAY = 100  # 0.1 s


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

        # Keyboard shortcuts

        for shortcut, action in [
            ("<", self.controls.do_previous),
            (" ", self.controls.do_play_pause),
            (">", self.controls.do_next),
            ("ctrl + p", self.controls.do_previous),
            ("ctrl + n", self.controls.do_next),
            ("ctrl + s", self.controls.do_stop),
        ]:
            tmp = QtGui.QShortcut(self)
            tmp.setKey(shortcut)
            tmp.activated.connect(action)

        self.key_listener = keyboard.Listener(on_press=self.do_hadle_keypress)
        self.key_listener.start()

    def do_hadle_keypress(self, key):
        if key == keyboard.Key.media_previous:
            self.controls.do_previous()
        elif key == keyboard.Key.media_play_pause:
            self.controls.do_play_pause()
        elif key == keyboard.Key.media_next:
            self.controls.do_next()

    def update_ui(self) -> None:
        self.playlist.update_ui()
        self.song_info.update_ui()
        self.navigator.update_ui()
        self.browser.update_ui()
        self.controls.update_ui()

    def closeEvent(self, event):
        self.player.quit()
        self.key_listener.stop()

        QtWidgets.QWidget.closeEvent(self, event)
