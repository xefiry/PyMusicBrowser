from peewee import fn

from ..database.song import Song

INCREMENT = 5


class Playlist:
    def __init__(self) -> None:
        self.song_list: list[Song] = []
        self.current_song: int = -1
        self.populate(INCREMENT)

    def populate(self, nb_elem: int) -> None:
        if self.current_song == -1:
            self.current_song = 0

        for _ in range(nb_elem):
            song = Song.select().order_by(fn.Random()).get()
            self.song_list.append(song)

    def __str__(self) -> str:
        return f"{self.current_song} - {self.song_list}"

    def print(self) -> None:
        for i, j in enumerate(self.song_list):
            if i == self.current_song:
                indent = ">"
            else:
                indent = " "
            print(f"{indent} {i} - {j}")
        print()

    def get_current(self) -> Song | None:
        if self.current_song == -1 and len(self.song_list) > 0:
            self.current_song = 0

        if self.current_song >= 0 and self.current_song < len(self.song_list):
            return self.song_list[self.current_song]
        else:
            return None

    def previous(self) -> Song | None:
        if self.current_song >= 0:
            self.current_song -= 1

        if self.current_song >= 0:
            return self.song_list[self.current_song]
        else:
            return None

    def next(self) -> Song:
        self.current_song += 1

        # If we don't have at least INCREMENT songs from the curent one
        # we add one>
        if len(self.song_list) - self.current_song < INCREMENT:
            self.populate(1)

        return self.song_list[self.current_song]
