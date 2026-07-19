import base64

from pynput import keyboard
from PySide6 import QtGui
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QSplashScreen,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from .. import database
from ..database.setting import Key, Setting
from ..player import Player
from .browser import BrowserWidget
from .controls import ControlsWidget
from .directory_picker import DirectoryPicker
from .playlist import PlaylistWidget
from .song_info import SongInfoWidget

UPDATE_DELAY = 100  # 0.1 s


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        icon = QIcon.fromTheme(QIcon.ThemeIcon.AudioCard)

        self.setWindowIcon(icon)
        self.setWindowTitle("PyMusicBrowser")

        self.player = Player()

        # UI content

        self.playlist = PlaylistWidget(self, self.player)
        self.song_info = SongInfoWidget(self, self.player)
        self.browser = BrowserWidget(self, self.player)
        self.controls = ControlsWidget(self, self.player)

        # UI building => menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.action_rescan = QtGui.QAction("Rescan database")
        self.menu_bar.addAction(self.action_rescan)

        # UI building => Side = Playlist + Song info

        side_widget = QWidget()
        side_widget.setFixedWidth(300)

        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)
        side_widget.setLayout(side_layout)

        side_layout.addWidget(self.playlist)
        side_layout.addWidget(self.song_info)

        # UI building => Top = Browser + Side

        top_widget = QWidget()

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        top_widget.setLayout(top_layout)

        top_layout.addWidget(self.browser)
        top_layout.addWidget(side_widget)

        # UI building => Main = Top + Controls

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)

        main_layout.addWidget(top_widget)
        main_layout.addWidget(self.controls)

        # Tray icon/menu

        self.menu = QMenu()
        self.quit_action = QAction(
            "Quit", icon=QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit)
        )
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.quit_action)

        self.tray = QSystemTrayIcon(icon=icon, parent=self, visible=True)
        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.do_handle_tray_click)

        # Periodic update of the UI

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(UPDATE_DELAY)

        # Connect UI

        self.action_rescan.triggered.connect(self.do_scan)

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

        # get geometry/state from settings
        geometry = Setting.get_value(Key.UI_GEOMETRY)
        state = Setting.get_value(Key.UI_STATE)

        # if it exists, use it
        if geometry != "":
            self.restoreGeometry(base64.b64decode(geometry.encode("utf-8")))
        if state != "":
            self.restoreState(base64.b64decode(state.encode("utf-8")))

    def quit(self) -> None:
        # if the window is hidde, first show it
        # if self.isHidden():
        self.show()
        self.close()

    def do_handle_tray_click(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.setVisible(not self.isVisible())

    def update_ui(self) -> None:
        self.playlist.update_ui()
        self.song_info.update_ui(self.tray)
        self.controls.update_ui()
        self.browser.update_ui()

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

            splash = QSplashScreen()
            splash.show()
            splash.showMessage("Database scan in progress")
            database.scan(dir_list)
            splash.finish(self)

            # restart updating
            self.timer.start()

        del picker

        if not database.has_songs():
            QMessageBox.information(
                self,
                "Empty database",
                "There are no songs in the database. Please scan another directory.",
            )

        # after rescanning, we update browser data
        self.browser.update_data()

        # and we clean playlist from non existent files
        self.player.playlist.clean()

    def closeEvent(self, event):
        self.player.quit()
        self.key_listener.stop()

        # get current geometry/state as utf-8 str
        geometry = base64.b64encode(self.saveGeometry().data()).decode("utf-8")
        state = base64.b64encode(self.saveState().data()).decode("utf-8")

        # and save them in settings
        Setting.upsert(Key.UI_GEOMETRY, geometry)
        Setting.upsert(Key.UI_STATE, state)

        QWidget.closeEvent(self, event)
