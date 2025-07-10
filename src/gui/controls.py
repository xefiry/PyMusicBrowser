from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon

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
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)

        self.setMinimumWidth(600)
        self.setFixedHeight(60)

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

    def update_ui(self) -> None:
        pass

    def set_play_button(self, is_playing: bool) -> None:
        if is_playing:
            icon = "pause"
        else:
            icon = "play"

        self.play_button.setIcon(BUTTON_ICON[icon])

    def get_volume(self) -> int:
        return self.volume_slider.value()

    def set_volume(self, volume: int) -> None:
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

    def get_time(self) -> int:
        return self.time_slider.value()

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
