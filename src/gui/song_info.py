from PySide6 import QtCore, QtGui, QtWidgets

from ..database import utils
from ..player import Player


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

            # image = QtGui.QPixmap(song.get)
            image_data = utils.get_cover(str(song.file_path))
            pixmap = QtGui.QPixmap()

            if image_data is not None:
                pixmap.loadFromData(image_data.read())
                pixmap = pixmap.scaled(300, 300)

            self.song_cover.setPixmap(pixmap)

            self.song_info.setText(f"""{song.track} - {song.name}
{song.album.name}
{song.artist.name}""")
