from PySide6 import QtWidgets

from ..database.album import Album
from ..database.artist import Artist
from ..database.song import Song
from ..player import Player

ITEM_TYPE = -1
ITEM_ID = -2


class BrowserWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setMinimumWidth(600)

        # Build UI

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.song_list = QtWidgets.QTreeWidget()
        self.song_list.setHeaderHidden(True)
        self.song_list.setColumnCount(1)
        layout.addWidget(self.song_list)

        for artist in (
            Artist.select(Artist.id, Artist.name)  # type: ignore
            .distinct()
            .join(Album)
            .order_by(Artist.name)
        ):
            artist_item = QtWidgets.QTreeWidgetItem()
            artist_item.setText(0, str(artist.name))
            artist_item.setData(0, ITEM_TYPE, "artist")
            artist_item.setData(0, ITEM_ID, artist.get_id())
            self.song_list.addTopLevelItem(artist_item)

            for album in (
                Album.select()
                .where(Album.artist == artist)
                .order_by(Album.year, Album.name)
            ):
                album_item = QtWidgets.QTreeWidgetItem()
                album_item.setText(0, f"[{album.year}] {album.name}")
                album_item.setData(0, ITEM_TYPE, "album")
                album_item.setData(0, ITEM_ID, album.get_id())
                artist_item.addChild(album_item)

                for song in (
                    Song.select()
                    .where(Song.album == album)
                    .order_by(Song.disk, Song.track, Song.name)
                ):
                    song_item = QtWidgets.QTreeWidgetItem()
                    song_item.setText(0, f"{song.track} - {song.name}")
                    song_item.setData(0, ITEM_TYPE, "song")
                    song_item.setData(0, ITEM_ID, song.get_id())
                    album_item.addChild(song_item)

            artist_item.setExpanded(True)

        # Connect UI

        self.song_list.itemActivated.connect(self.do_play_song)

        # Status member variables

        # ...

    def update_ui(self) -> None:
        pass

    def do_play_song(self, item: QtWidgets.QTreeWidgetItem) -> None:
        if item.data(0, ITEM_TYPE) == "song":
            song_id = item.data(0, ITEM_ID)
            self.player.add_song(song_id)
        elif item.data(0, ITEM_TYPE) == "album":
            album_id = item.data(0, ITEM_ID)
            self.player.add_album(album_id)
