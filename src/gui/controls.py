from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIcon

from ..database.setting import Setting
from ..player import Player, State

BUTTON_ICON = {
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


class ControlsWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setMinimumWidth(600)
        self.setFixedHeight(60)

        # Build UI

        layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(layout)

        self.prev_button = QtWidgets.QPushButton("prev")
        self.play_button = QtWidgets.QPushButton("play")
        self.next_button = QtWidgets.QPushButton("next")
        self.stop_button = QtWidgets.QPushButton("stop")

        for b in [
            self.prev_button,
            self.play_button,
            self.next_button,
            self.stop_button,
        ]:
            b.setIcon(BUTTON_ICON[b.text()])
            b.setText("")
            b.setFixedSize(40, 40)
            b.setFlat(True)
            layout.addWidget(b)

        self.volume_button = QtWidgets.QPushButton()
        self.volume_button.setIcon(BUTTON_ICON["volHigh"])
        self.volume_button.setFixedSize(25, 25)
        self.volume_button.setFlat(True)
        layout.addWidget(self.volume_button)

        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setTickInterval(25)
        self.volume_slider.setPageStep(2)
        self.volume_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        layout.addWidget(self.volume_slider)

        self.volume_label = QtWidgets.QLabel("100 %")
        self.volume_label.setFixedWidth(40)
        layout.addWidget(self.volume_label)

        self.time_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(self.time_slider)

        self.time_label = QtWidgets.QLabel("0:00 / 0:00")
        layout.addWidget(self.time_label)

        # Connect UI

        self.play_button.pressed.connect(self.do_play_pause)
        self.prev_button.pressed.connect(self.do_previous)
        self.next_button.pressed.connect(self.do_next)
        self.stop_button.pressed.connect(self.do_stop)
        self.volume_slider.valueChanged.connect(self.do_change_volume)
        self.volume_button.pressed.connect(self.do_mute_volume)
        self.time_slider.valueChanged.connect(self.do_change_time)

        # Keyboard shortcuts

        for shortcut in [
            (" ", self.do_play_pause),
            ("<", self.do_previous),
            (">", self.do_next),
        ]:
            new = QtGui.QShortcut(self)
            new.setKey(shortcut[0])
            new.activated.connect(shortcut[1])

        # Status member variables

        self.previous_volume = int(Setting.get_value("volume", "100"))
        self.set_volume(self.previous_volume)

    def update_ui(self) -> None:
        state = self.player.state

        new_icon = "pause" if state == State.PLAY else "play"
        self.play_button.setIcon(BUTTON_ICON[new_icon])

        self.time_slider.setEnabled(state != State.STOP)

        self.set_time(self.player.get_current_time())

    def do_play_pause(self) -> None:
        self.player.play_pause()

    def do_previous(self) -> None:
        self.player.previous()

    def do_next(self) -> None:
        self.player.next()

    def do_stop(self) -> None:
        self.player.stop()

    def do_change_volume(self) -> None:
        volume = self.volume_slider.value()
        self.set_volume(volume)

    def do_mute_volume(self) -> None:
        volume = self.player.get_volume()
        if volume != 0:
            self.previous_volume = volume
            self.set_volume(0)
        else:
            self.set_volume(self.previous_volume)

    def do_change_time(self) -> None:
        time = self.time_slider.value()
        self.player.seek(time)

    def set_volume(self, volume: int) -> None:
        self.player.set_volume(volume)
        Setting.upsert("volume", str(volume))

        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(volume)
        self.volume_slider.blockSignals(False)
        self.volume_label.setText(f"{volume} %")

        if volume > 66:
            strength = "volHigh"
        elif volume > 33:
            strength = "volMedium"
        elif volume > 0:
            strength = "volLow"
        else:
            strength = "volMuted"

        self.volume_button.setIcon(BUTTON_ICON[strength])

    def set_time(self, time: tuple[int, int]) -> None:
        self.time_slider.blockSignals(True)
        self.time_slider.setValue(time[0])
        self.time_slider.setRange(0, time[1])
        self.time_slider.blockSignals(False)
        self.time_label.setText(f"{s_to_t(time[0])} / {s_to_t(time[1])}")


def s_to_t(seconds: float) -> str:
    """Convert a number of seconds to displayable time"""
    result: str = ""

    h = seconds // 3600
    seconds = seconds % 3600

    s = int(seconds % 60)
    m = int(seconds // 60)

    if h > 0:
        result = f"{h}:{m:02}:{s:02}"
    else:
        result = f"{m}:{s:02}"

    return result
