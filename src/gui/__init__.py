import sys

from PySide6 import QtCore, QtWidgets

from ..database.setting import Setting
from ..player import Player, State
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

        self.controls = ControlsWidget(self)
        main_layout.addWidget(self.controls)

        # Controls connection

        self.controls.play_button.pressed.connect(self.do_play_pause)
        self.controls.prev_button.pressed.connect(self.do_previous)
        self.controls.next_button.pressed.connect(self.do_next)
        self.controls.stop_button.pressed.connect(self.do_stop)
        self.controls.volume_slider.valueChanged.connect(self.do_change_volume)
        self.controls.volume_button.pressed.connect(self.do_mute_volume)
        self.controls.time_slider.valueChanged.connect(self.do_change_time)

        # Status member variables
        self.previous_volume = int(Setting.get_value("volume", "100"))
        self.set_volume(self.previous_volume)

        self.current_song = -1

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(UPDATE_DELAY)

        self.update_ui()

    def __del__(self):
        self.player.quit()

    def do_play_pause(self) -> None:
        self.player.play_pause()

    def do_previous(self) -> None:
        self.player.previous()

    def do_next(self) -> None:
        self.player.next()

    def do_stop(self) -> None:
        self.player.stop()

    def set_volume(self, volume: int) -> None:
        self.controls.set_volume(volume)
        self.player.set_volume(volume)
        Setting.upsert("volume", str(volume))

    def do_change_volume(self) -> None:
        volume = self.controls.get_volume()
        self.set_volume(volume)

    def do_change_time(self) -> None:
        time = self.controls.get_time()
        self.player.seek(time)

    def do_mute_volume(self) -> None:
        volume = self.player.get_volume()
        if volume != 0:
            self.previous_volume = volume
            self.set_volume(0)
        else:
            self.set_volume(self.previous_volume)

    def update_ui(self) -> None:
        state = self.player.state

        self.controls.set_play_button(state == State.PLAY)

        if state == State.STOP:
            self.controls.time_slider.setEnabled(False)
        else:
            self.controls.time_slider.setEnabled(True)

        self.controls.set_time(self.player.get_current_time())

        song_list = self.player.get_song_list()
        if self.current_song != song_list[1]:
            print("updating playlist")
            self.playlist.set_list(song_list)
            self.current_song = song_list[1]
