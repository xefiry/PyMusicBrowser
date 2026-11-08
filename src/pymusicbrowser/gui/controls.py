from PySide6 import QtCore, QtWidgets

from ..database.setting import Key, Setting
from ..player import Player, State
from . import utils
from .icons import ICON


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
            b.setIcon(ICON[b.text()])
            b.setText("")
            b.setFixedSize(40, 40)
            b.setFlat(True)
            layout.addWidget(b)

        self.volume_button = QtWidgets.QPushButton()
        self.volume_button.setIcon(ICON["volHigh"])
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

        # Volume

        self.volume = int(Setting.get_value(Key.VOLUME, "50"))
        self.muted = Setting.get_value(Key.VOLUME_MUTED, "False") == "True"
        self.set_volume(self.volume, self.muted)

    def update_ui(self) -> None:
        state = self.player.state

        new_icon = "pause" if state == State.PLAY else "play"
        self.play_button.setIcon(ICON[new_icon])

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
        self.set_volume(self.volume_slider.value(), self.muted)

    def do_mute_volume(self) -> None:
        self.muted = not self.muted
        self.set_volume(self.volume, self.muted)

    def do_change_time(self) -> None:
        time = self.time_slider.value()
        self.player.seek(time)

    def set_volume(self, volume: int, muted: bool) -> None:
        self.volume = volume
        self.muted = muted
        Setting.upsert(Key.VOLUME, str(volume))
        Setting.upsert(Key.VOLUME_MUTED, str(muted))

        if self.muted:
            self.player.set_volume(0)
        else:
            self.player.set_volume(volume)

        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(volume)
        self.volume_slider.blockSignals(False)
        self.volume_label.setText(f"{volume} %")

        if muted:
            strength = "volMuted"
        elif volume > 66:
            strength = "volHigh"
        elif volume > 33:
            strength = "volMedium"
        else:
            strength = "volLow"

        self.volume_button.setIcon(ICON[strength])

    def set_time(self, time: tuple[int, int]) -> None:
        self.time_slider.blockSignals(True)
        self.time_slider.setValue(time[0])
        self.time_slider.setRange(0, time[1])
        self.time_slider.blockSignals(False)
        self.time_label.setText(f"{utils.s_to_t(time[0])} / {utils.s_to_t(time[1])}")
