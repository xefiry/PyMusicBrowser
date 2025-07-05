from peewee import fn

from ..database.song import Song
from ..database.setting import Setting

INCREMENT = 5


class Playlist:
    def __init__(self) -> None:
        self.song_list: list[Song] = []
        # if current_song == 1, no current song is selected
        self.current_song: int = -1
        self.load()
        self.populate(0)

    def populate(self, nb_elem: int) -> None:
        # if no current song, we set it to the start of the list
        if self.current_song == -1:
            self.current_song = 0

        for _ in range(nb_elem):
            song = Song.select().order_by(fn.Random()).get()
            self.song_list.append(song)

        # If we don't have at least INCREMENT songs from the curent one we add some
        while len(self.song_list) - self.current_song < INCREMENT:
            song = Song.select().order_by(fn.Random()).get()
            self.song_list.append(song)

    def __str__(self) -> str:
        return f"{self.current_song} - {self.song_list}"

    def save(self) -> None:
        cur = self.current_song
        songs = ",".join([str(song.get_id()) for song in self.song_list])

        Setting.upsert("playlist", f"{cur}|{songs}")

    def load(self) -> None:
        playlist = Setting.get_value("playlist")
        cur, songs = playlist.split("|")

        self.current_song = int(cur)

        for song_id in songs.split(","):
            self.song_list.append(Song.get_by_id(song_id))

    def print(self) -> None:
        min_idx = max(self.current_song - INCREMENT, 0)
        max_idx = min(self.current_song + INCREMENT + 1, len(self.song_list))

        if min_idx > 0:
            print("...")

        for i, j in enumerate(self.song_list[min_idx:max_idx]):
            if self.current_song == i + min_idx:
                indent = ">"
            else:
                indent = " "
            print(f"{indent} {i + min_idx:3} - {j}")

        if max_idx < len(self.song_list):
            print("...")
        print()

    def get_current(self) -> Song:
        # if there is no current song selected and there are songs in the list
        # we set the first song as current
        if self.current_song == -1 and len(self.song_list) > 0:
            self.current_song = 0

        return self.song_list[self.current_song]

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

    def remove(self, song_nb: int) -> bool:
        """returns true if the removed song was the current one"""
        s = self.song_list[song_nb]
        self.song_list.remove(s)

        self.populate(0)

        if song_nb < self.current_song:
            self.current_song -= 1
        elif song_nb == self.current_song:
            return True

        return False
