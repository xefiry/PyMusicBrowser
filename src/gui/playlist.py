from PySide6 import QtGui, QtWidgets
from PySide6.QtGui import QKeyEvent, QKeySequence

from ..database.song import Song
from ..player import Player

SONG_INDEX = -1
SONG_ID = -2


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

        # ToDo: enable drag&drop and handle playlist update
        _mode = QtWidgets.QAbstractItemView.DragDropMode.InternalMove
        self.song_list.setDragDropMode(_mode)

        # Connect UI

        self.song_list.currentItemChanged.connect(self.do_select_item)
        self.song_list.itemActivated.connect(self.do_play_song)
        self.song_list.dropEvent = self.do_drop

        # Status member variables

        self.playlist_status = (-1, -1)
        self.selected_item_index = 0
        self.current_song_index = 0

    def update_ui(self, force: bool = False) -> None:
        song_list = self.player.get_song_list()

        playlist_status = (len(song_list[0]), song_list[1])

        # if playlist has changed or if we force the update
        if self.playlist_status != playlist_status or force:
            self.song_list.blockSignals(True)
            self.set_list(song_list)
            self.song_list.blockSignals(False)
            self.playlist_status = playlist_status

            self.song_list.setCurrentRow(self.selected_item_index)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if isinstance(event, QKeyEvent) and event == QKeySequence.StandardKey.Delete:
            self.do_remove_song()

    def do_select_item(self, item: QtWidgets.QListWidgetItem) -> None:
        index = self.song_list.indexFromItem(item).row()
        self.selected_item_index = index

    def do_play_song(self, item: QtWidgets.QListWidgetItem) -> None:
        index = self.song_list.indexFromItem(item).row()
        self.player.select_song(index)

    def do_remove_song(self) -> None:
        indexes = self.song_list.selectedIndexes()
        if len(indexes) == 0:
            return
        index = indexes[0].row()

        self.player.remove_song(index)

        self.update_ui(True)

    def do_drop(self, event: QtGui.QDropEvent) -> None:
        # call default event handler
        QtWidgets.QListWidget.dropEvent(self.song_list, event)

        song_id_list = []
        new_song_index = -1
        new_selected_index = -1

        for i in range(self.song_list.count()):
            # get the song from the list
            song = self.song_list.item(i)

            # get the song ID, and add it to the list
            song_id = song.data(SONG_ID)
            song_id_list.append(song_id)

            # get the index from data
            song_index = song.data(SONG_INDEX)

            # if the song index in the data is the current one, we save it
            if song_index == self.current_song_index:
                new_song_index = i

            # if the song index in the data is the selected song
            # and it has not been already found, update it with the new one
            if song_index == self.selected_item_index and new_selected_index == -1:
                new_selected_index = i

        # update the selected index
        self.selected_item_index = new_selected_index

        # create the list of songs ID
        items = ",".join(map(str, song_id_list))

        # Load the new playlist order
        self.player.playlist.load(f"{new_song_index}|{items}")

        # Force UI update
        self.update_ui(True)

    def set_list(self, song_list: tuple[list[Song], int]) -> None:
        songs, self.current_song_index = song_list

        self.song_list.clear()
        for nb, song in enumerate(songs):
            prefix = "⏵" if nb == self.current_song_index else " "
            item = QtWidgets.QListWidgetItem(self.song_list)
            item.setData(SONG_INDEX, nb)
            item.setData(SONG_ID, song.get_id())
            item.setText(f"{prefix} {song}")
