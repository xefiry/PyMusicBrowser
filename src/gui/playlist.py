from PySide6 import QtWidgets
from PySide6.QtGui import QKeyEvent, QKeySequence


class PlaylistWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self.setFixedWidth(300)
        self.setMinimumHeight(500)

        layout = QtWidgets.QVBoxLayout(self)

        self.setLayout(layout)

        self.song_list = QtWidgets.QListWidget()
        layout.addWidget(self.song_list)

        self.song_list.itemActivated.connect(self.itemActivated)

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent) and event == QKeySequence.StandardKey.Delete:
            index = self.song_list.selectedIndexes()
            print(event, index)

    def itemActivated(self, item) -> None:
        index = self.song_list.indexFromItem(item).row()

        print(f"itemActivated : {index} - {item.text()}")

    def set_list(self, song_list: tuple[list[str], int]) -> None:
        songs, index = song_list

        songs[index] = "> " + songs[index]

        self.song_list.clear()
        for song in songs:
            item = QtWidgets.QListWidgetItem(self.song_list)
            item.setText(song)


# for dev purposes
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    widget = PlaylistWidget()
    tmp = [f"element {i}" for i in range(30)]
    widget.set_list((tmp, 10))
    widget.show()
    app.exec()
