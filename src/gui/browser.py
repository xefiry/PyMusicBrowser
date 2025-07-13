from PySide6 import QtWidgets

from .. import database
from ..database.album import Album
from ..database.song import Song
from ..player import Player

DATA = -1


class BrowserWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setMinimumWidth(600)

        # Build UI

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        layout.addWidget(self.search_bar)

        self.song_list = QtWidgets.QTreeWidget()
        self.song_list.setHeaderHidden(True)
        self.song_list.setColumnCount(1)
        layout.addWidget(self.song_list)

        for artist in database.get_artists(has_album=True):
            artist_item = QtWidgets.QTreeWidgetItem()
            artist_item.setText(0, str(artist.name))
            artist_item.setData(0, DATA, artist)
            self.song_list.addTopLevelItem(artist_item)

            for album in database.get_albums(artist):
                album_item = QtWidgets.QTreeWidgetItem()
                album_item.setText(0, f"[{album.year}] {album.name}")
                album_item.setData(0, DATA, album)
                artist_item.addChild(album_item)

                for song in database.get_songs(album):
                    song_item = QtWidgets.QTreeWidgetItem()
                    song_item.setText(0, f"{song.track} - {song.name}")
                    song_item.setData(0, DATA, song)
                    album_item.addChild(song_item)

            artist_item.setExpanded(True)

        # Connect UI

        self.search_bar.textChanged.connect(self.do_search)
        self.song_list.itemActivated.connect(self.do_play_song)

        # Status member variables

        # ...

    def update_ui(self) -> None:
        pass

    def do_search(self, input: str) -> None:
        hide_song: bool
        hide_album: bool
        hide_artist: bool

        root = self.song_list.invisibleRootItem()

        for i in range(root.childCount()):
            artist = root.child(i)

            hide_artist = True

            for j in range(artist.childCount()):
                album = artist.child(j)

                hide_album = True

                for k in range(album.childCount()):
                    song = album.child(k)
                    song_data: Song = song.data(0, DATA)

                    hide_song = not song_data.match(input)
                    song.setHidden(hide_song)

                    # don't hide album if we show (not hidden) at least one song
                    hide_album = hide_album and hide_song

                album.setHidden(hide_album)

                # expand album section if input is not empty and album is not hidden
                album.setExpanded(input != "" and not hide_album)

                # don't hide artist if we show (not hidden) at least one album
                hide_artist = hide_artist and hide_album

            artist.setHidden(hide_artist)

    def do_play_song(self, item: QtWidgets.QTreeWidgetItem) -> None:
        data = item.data(0, DATA)

        # ToDo: add possibility to add whole album artist songs

        if type(data) is Song:
            self.player.add_song(data.get_id())
        elif type(data) is Album:
            self.player.add_album(data.get_id())
