from .. import database
from ..database.setting import Key, Setting
from ..database.song import Song

INCREMENT = 5


class Playlist:
    def __init__(self) -> None:
        self.song_list: list[Song] = []
        # if current_song == 1, no current song is selected
        self.current_song: int = -1
        self.load()
        self.populate(0)

    def populate(self, nb_elem: int) -> None:
        # if there are no songs in the database, do nothing
        if not database.has_songs():
            return

        # if no current song, we set it to the start of the list
        if self.current_song == -1:
            self.current_song = 0

        for _ in range(nb_elem):
            song = Song.get_random()
            self.song_list.append(song)

        # If we don't have at least INCREMENT songs from the curent one we add some
        while len(self.song_list) - self.current_song < INCREMENT:
            song = Song.get_random()
            self.song_list.append(song)

    def __str__(self) -> str:
        return f"{self.current_song} - {self.song_list}"

    def save(self) -> None:
        # don't save if playlist is empty
        if len(self.song_list) > 0:
            cur = self.current_song
            songs = ",".join([str(song.get_id()) for song in self.song_list])
            Setting.upsert(Key.PLAYLIST, f"{cur}|{songs}")

    def load(self, playlist: str = "") -> None:
        if playlist == "":
            playlist = Setting.get_value(Key.PLAYLIST)

        if playlist == "":
            return

        cur, songs = playlist.split("|")

        self.current_song = int(cur)

        self.song_list.clear()

        for song_id in songs.split(","):
            self.song_list.append(Song.get_by_id(song_id))

    def get_current(self) -> Song | None:
        # if playlist is empty, return None
        if len(self.song_list) == 0:
            return None

        # if there is no current song selected and there are songs in the list
        # we set the first song as current
        if self.current_song == -1 and len(self.song_list) > 0:
            self.current_song = 0

        return self.song_list[self.current_song]

    # TODO Calling previous replays the same song if time position is > N seconds (to define)
    def previous(self) -> bool:
        """Returns true if we could go back, false if not (at start of playlist)"""
        # If we are in the list, we go backward
        if self.current_song >= 0:
            self.current_song -= 1

        # if we are still in the list after that, we return true
        return self.current_song >= 0

    def next(self) -> None:
        self.current_song += 1
        self.populate(0)

    def select(self, song_nb: int) -> None:
        self.current_song = song_nb
        self.populate(0)

    def add_next(self, song: Song) -> None:
        self.song_list.insert(self.current_song + 1, song)

    def remove(self, song_nb: int) -> bool:
        """returns true if the removed song was the current one"""
        self.song_list.pop(song_nb)

        self.populate(0)

        if song_nb < self.current_song:
            self.current_song -= 1
        elif song_nb == self.current_song:
            return True

        return False

    def clean(self) -> None:
        # loop on reverse list
        for index, song in reversed(list(enumerate(self.song_list))):
            if not Song.file_exists(song.file_path):
                self.song_list.pop(index)

                # if the removed song is the current song or before
                if index <= self.current_song:
                    # we decrement the current song to follow
                    self.current_song -= 1

        self.populate(0)
