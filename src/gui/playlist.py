from PySide6 import QtWidgets
from PySide6.QtGui import QKeyEvent, QKeySequence

from ..player import Player


class PlaylistWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setFixedWidth(300)
        self.setMinimumHeight(500)

        # Build UI

        layout = QtWidgets.QVBoxLayout(self)

        self.setLayout(layout)

        self.song_list = QtWidgets.QListWidget()
        layout.addWidget(self.song_list)

        # Connect UI

        self.song_list.currentItemChanged.connect(self.do_select_item)
        self.song_list.itemActivated.connect(self.do_play_song)

        # Status member variables

        self.playlist_status = (-1, -1)
        self.current_item = 0

    def update_ui(self, force: bool = False) -> None:
        song_list = self.player.get_song_list()

        playlist_status = (len(song_list[0]), song_list[1])

        # if playlist has changed or if we force the update
        if self.playlist_status != playlist_status or force:
            print("updating playlist")
            self.set_list(song_list)
            self.playlist_status = playlist_status

            self.song_list.setCurrentRow(self.current_item)

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent) and event == QKeySequence.StandardKey.Delete:
            self.do_remove_song()

    def do_select_item(self, item) -> None:
        index = self.song_list.indexFromItem(item).row()
        self.current_item = index

    def do_play_song(self, item) -> None:
        index = self.song_list.indexFromItem(item).row()
        self.player.select_song(index)

    def do_remove_song(self) -> None:
        indexes = self.song_list.selectedIndexes()
        if len(indexes) == 0:
            return
        index = indexes[0].row()

        self.player.remove_song(index)

    def set_list(self, song_list: tuple[list[str], int]) -> None:
        songs, index = song_list

        songs[index] = "> " + songs[index]

        self.song_list.clear()
        for song in songs:
            item = QtWidgets.QListWidgetItem(self.song_list)
            item.setText(song)
