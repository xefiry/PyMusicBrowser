from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon

BUTTON_ICON = {
    "play": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart),
    "pause": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause),
    "prev": QIcon.fromTheme(QIcon.ThemeIcon.MediaSkipBackward),
    "next": QIcon.fromTheme(QIcon.ThemeIcon.MediaSkipForward),
    "stop": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop),
    "volMuted": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMuted),
    "volLow": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeLow),
    "volMedium": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMedium),
    "volHigh": QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeHigh),
}


class ControlsWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
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

        _orientation = QtCore.Qt.Orientation.Horizontal

        self.volume_button = QtWidgets.QPushButton()
        self.volume_button.setIcon(BUTTON_ICON["volHigh"])
        self.volume_button.setFixedSize(25, 25)
        self.volume_button.setFlat(True)
        layout.addWidget(self.volume_button)

        self.volume_slider = QtWidgets.QSlider(_orientation)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(100)
        layout.addWidget(self.volume_slider)

        self.volume_label = QtWidgets.QLabel("100%")
        layout.addWidget(self.volume_label)

        self.time_slider = QtWidgets.QSlider(_orientation)
        layout.addWidget(self.time_slider)

        self.time_label = QtWidgets.QLabel("0:00 / 0:00")
        layout.addWidget(self.time_label)
