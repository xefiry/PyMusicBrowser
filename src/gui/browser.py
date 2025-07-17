from PySide6 import QtWidgets

from .. import database
from ..database.album import Album
from ..database.song import Song
from ..player import Player
from . import utils
from .navigation import NavigationWidget

DATA = -1


class BrowserWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setMinimumWidth(800)

        # Build UI

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.navigation = NavigationWidget(self, self.player)
        layout.addWidget(self.navigation)

        center_widget = QtWidgets.QWidget()
        layout.addWidget(center_widget)

        center_layout = QtWidgets.QVBoxLayout(center_widget)
        center_widget.setLayout(center_layout)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search library ...")
        self.search_bar.setClearButtonEnabled(True)
        center_layout.addWidget(self.search_bar)

        self.song_list = QtWidgets.QTreeWidget()
        self.song_list.setHeaderHidden(True)
        self.song_list.setColumnCount(2)
        self.song_list.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        )
        center_layout.addWidget(self.song_list)

        # Connect UI

        self.navigation.item_list.itemSelectionChanged.connect(self.do_search)
        self.search_bar.textChanged.connect(self.do_search)
        self.song_list.itemActivated.connect(self.do_play_song)

        # Function calls

        self.update_data()

    def update_data(self) -> None:
        self.navigation.update_data()

        self.song_list.clear()

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
                    song_item.setText(1, utils.s_to_t(song.duration))
                    song_item.setData(0, DATA, song)
                    album_item.addChild(song_item)

            artist_item.setExpanded(True)

        # Update column sizez to fit content
        self.song_list.resizeColumnToContents(0)
        self.song_list.resizeColumnToContents(1)

    def do_search(self) -> None:  # TODO improve performances
        hide_song: bool
        hide_album: bool
        hide_artist: bool
        match_search: bool
        match_filter: bool
        filter_category: str = ""
        filter_value: str = ""

        # get search strins from search bar
        search_value = self.search_bar.text()

        # and navigation bar
        filter_category, filter_value = self.navigation.get_selected()

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

                    # check if the song matches with search input
                    # if input is empty, it does matche
                    match_search = song_data.match(search_value)

                    # check if the song matches with filter set by navigator
                    # if match filter is empty, it does match
                    match_filter = (
                        filter_category == ""
                        or (
                            filter_category == "Album Artist"
                            and str(song_data.album.artist) == filter_value
                        )
                        or (
                            filter_category == "Song Artist"
                            and str(song_data.artist) == filter_value
                        )
                        or (
                            filter_category == "Genre"
                            and str(song_data.genre) == filter_value
                        )
                        or (
                            filter_category == "Year"
                            and str(song_data.year) == filter_value
                        )
                    )

                    # hide the song if it does not match with both search and filter
                    hide_song = not (match_search and match_filter)

                    song.setHidden(hide_song)

                    # don't hide album if we show (not hidden) at least one song
                    hide_album = hide_album and hide_song

                album.setHidden(hide_album)

                # expand album section if input is not empty and album is not hidden
                album.setExpanded(input != "" and not hide_album)

                # don't hide artist if we show (not hidden) at least one album
                hide_artist = hide_artist and hide_album

            artist.setHidden(hide_artist)

    def do_focus_search_bar(self) -> None:
        self.search_bar.setFocus()
        self.search_bar.selectAll()

    def do_focus_playing_song(self) -> None:
        playing_song = self.player.playlist.get_current()
        found: bool = False

        if playing_song is None:
            return

        playing_song_id = playing_song.get_id()

        # clear search bar to make sure we can see playing song in list
        self.search_bar.clear()

        # TODO also clear navigation search bar/filter

        root = self.song_list.invisibleRootItem()

        for i in range(root.childCount()):
            artist = root.child(i)

            for j in range(artist.childCount()):
                album = artist.child(j)
                album.setExpanded(False)

                # don't search in songs if we already found
                if not found:
                    for k in range(album.childCount()):
                        song = album.child(k)

                        if song.data(0, DATA).get_id() == playing_song_id:
                            # without this, successives call to do_focus_playing_song do not select the song
                            self.song_list.setCurrentItem(root.child(0))
                            self.song_list.clearSelection()
                            self.song_list.setCurrentItem(song)
                            self.song_list.setFocus()
                            found = True
                            break

    def do_play_song(self, item: QtWidgets.QTreeWidgetItem) -> None:
        # FIXME if item is an Artist, it plays next without adding any song
        self.queue_item(item)
        self.player.next()

    def do_queue_selected(self) -> None:
        # the items are reversed because queue_item adds next to current song
        for item in reversed(self.song_list.selectedItems()):
            self.queue_item(item)

    def queue_item(self, item: QtWidgets.QTreeWidgetItem) -> None:
        data = item.data(0, DATA)

        # TODO add possibility to add whole album artist songs

        if type(data) is Song:
            self.player.add_song(data)
        elif type(data) is Album:
            self.player.add_album(data)
