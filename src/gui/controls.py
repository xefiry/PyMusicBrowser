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

        self.volume_slider.valueChanged.connect(self.volume_changed)
        self.volume_button.clicked.connect(self.volume_muted)

        self.previous_volume = 0
        self.set_volume(100)

    def volume_muted(self) -> None:
        volume = self.get_volume()
        if volume != 0:
            self.previous_volume = volume
            self.set_volume(0)
        else:
            self.set_volume(self.previous_volume)

    def volume_changed(self) -> None:
        volume = self.get_volume()
        self.set_volume(volume)

    def get_volume(self) -> int:
        return self.volume_slider.value()

    def set_volume(self, volume: int) -> None:
        self.volume_slider.setValue(volume)
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


# for dev purposes
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    widget = ControlsWidget()
    widget.show()
    app.exec()
