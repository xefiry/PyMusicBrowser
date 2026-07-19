from PySide6.QtGui import QIcon

ICON = {
    "main": QIcon("src/icons/main.svg"),
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
