from PySide6 import QtCore, QtWidgets

from ..player import Player
from . import utils


class SongInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setFixedWidth(300)
        self.setFixedHeight(350)

        # Build UI

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.song_cover = QtWidgets.QLabel(text="SONG_COVER")
        self.song_cover.setFixedWidth(300)
        self.song_cover.setFixedHeight(300)
        layout.addWidget(self.song_cover)

        self.song_info = QtWidgets.QLabel(text="SONG_INFO")
        self.song_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.song_info.setFixedHeight(50)
        layout.addWidget(self.song_info)

        # Status member variables

        self.current_song_id = -1

    def update_ui(self) -> None:
        song = self.player.playlist.get_current()
        if song is not None and self.current_song_id != song.get_id():
            self.current_song_id = song.get_id()

            pixmap = utils.get_cover(song, 300)
            self.song_cover.setPixmap(pixmap)

            self.song_info.setText(f"""{song.track} - {song.name}
{song.album.name}
{song.artist.name}""")
