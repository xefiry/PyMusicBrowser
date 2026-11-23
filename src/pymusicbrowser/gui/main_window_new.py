from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QPushButton

from .icons import ICON
from .utils import get_child, load_widget_from_file

"""
- main_window: QMainWindow
  - main_widget: QWidget
    - top_widget: QWidget
      - navigation: QWidget
      - browser: QWidget
      - side_widget: QWidget
        - playlist: QWidget
        - song_info: QWidget
    - controls: QWidget
  - menu_bar: QMenuBar
    - menu_file: QMenu
      - action_rescan: QAction
"""


ICON = {
    "main": QIcon.fromTheme(QIcon.ThemeIcon.AudioCard),
    "quit": QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit),
    "clear": QIcon.fromTheme(QIcon.ThemeIcon.EditClear),
    "play": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart),
    "pause": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause),
    "prev": QIcon.fromTheme(QIcon.ThemeIcon.MediaSkipBackward),
    "next": QIcon.fromTheme(QIcon.ThemeIcon.MediaSkipForward),
    "stop": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop),
    "volHigh": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeHigh),
    "volMedium": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMedium),
    "volLow": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeLow),
    "volMuted": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMuted),
}


class MainWindow:
    def __init__(self) -> None:
        # Load UI
        self.ui = load_widget_from_file(
            "src/pymusicbrowser/gui/main_window.ui", QMainWindow
        )

        self.action_rescan = get_child(self.ui, QAction, "action_rescan")
        self.action_rescan.triggered.connect(self.do_scan)

        self.button_next = get_child(self.ui, QPushButton, "button_next")
        self.button_prev = get_child(self.ui, QPushButton, "button_prev")
        self.button_volume = get_child(self.ui, QPushButton, "button_volume")
        self.button_stop = get_child(self.ui, QPushButton, "button_stop")
        self.button_play = get_child(self.ui, QPushButton, "button_play")

    def show(self) -> None:
        self.ui.show()

    def do_scan(self) -> None:
        # TODO: write this
        print("do_scan")
