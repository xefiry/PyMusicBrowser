from pynput import keyboard
from PySide6 import QtCore, QtGui, QtWidgets

from .. import database
from ..database.setting import Key, Setting
from ..player import Player
from .browser import BrowserWidget
from .controls import ControlsWidget
from .directory_picker import DirectoryPicker
from .navigation import NavigationWidget
from .playlist import PlaylistWidget
from .song_info import SongInfoWidget

UPDATE_DELAY = 100  # 0.1 s


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        _icon = QtGui.QIcon.fromTheme(QtGui.QIcon.ThemeIcon.AudioCard)
        self.setWindowIcon(_icon)
        self.setWindowTitle("PyMusicBrowser")

        self.player = Player()

        # UI content

        self.playlist = PlaylistWidget(self, self.player)
        self.song_info = SongInfoWidget(self, self.player)
        self.navigator = NavigationWidget(self, self.player)
        self.browser = BrowserWidget(self, self.player)
        self.controls = ControlsWidget(self, self.player)

        # UI building => menu bar
        self.menu_bar = QtWidgets.QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.action_rescan = QtGui.QAction("Rescan database")
        self.menu_bar.addAction(self.action_rescan)

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

        # Connect UI

        self.action_rescan.triggered.connect(self.do_scan)
        self.navigator.filter_bar.textChanged.connect(self.browser.do_filter)

        # Keyboard shortcuts

        # TODO Add mouse prev/next for prev/next song
        for shortcut, action in [
            (" ", self.controls.do_play_pause),
            ("<", self.controls.do_previous),
            (">", self.controls.do_next),
            ("ctrl + s", self.controls.do_stop),
            ("ctrl + q", self.browser.do_queue_selected),
            ("ctrl + l", self.browser.do_focus_playing_song),
            ("ctrl + f", self.browser.do_focus_search_bar),
        ]:
            tmp = QtGui.QShortcut(self)
            tmp.setKey(shortcut)
            tmp.activated.connect(action)

        self.key_listener = keyboard.Listener(on_press=self.do_hadle_keypress)
        self.key_listener.start()

        # Function calls

        if not database.has_songs():
            self.do_scan()

    def update_ui(self) -> None:
        self.playlist.update_ui()
        self.song_info.update_ui()
        self.controls.update_ui()

    def do_hadle_keypress(self, key):
        if key == keyboard.Key.media_previous:
            self.controls.do_previous()
        elif key == keyboard.Key.media_play_pause:
            self.controls.do_play_pause()
        elif key == keyboard.Key.media_next:
            self.controls.do_next()
        elif key == keyboard.Key.media_stop:
            self.controls.do_stop()

    def do_scan(self) -> None:
        # open directory picker with known MUSIC_DIR setting
        setting = Setting.get_value(Key.MUSIC_DIR)

        if setting == "":
            dir_list = []
        else:
            dir_list = setting.split(";")

        picker = DirectoryPicker(self, dir_list)

        if picker.exec():
            # stop any playing music, and the UI updates
            self.player.stop()
            self.timer.stop()

            # store the obtained directory list in setting
            dir_list = picker.get_dir_list()
            Setting.upsert(Key.MUSIC_DIR, ";".join(dir_list))

            splash = QtWidgets.QSplashScreen()
            splash.show()
            splash.showMessage("Database scan in progress")
            database.scan(dir_list)
            splash.finish(self)

            # restart updating
            self.timer.start()

        del picker

        if not database.has_songs():
            QtWidgets.QMessageBox.information(
                self,
                "Empty database",
                "There are no songs in the database. Please scan another directory.",
            )

        # after rescanning, we update navigator and browser data
        self.navigator.update_data()
        self.browser.update_data()

        # and we clean playlist from non existent files
        self.player.playlist.clean()

    def closeEvent(self, event):
        self.player.quit()
        self.key_listener.stop()

        QtWidgets.QWidget.closeEvent(self, event)
