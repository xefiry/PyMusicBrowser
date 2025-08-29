import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from database import utils


def get_cover(song: str, size: int) -> QtGui.QPixmap:
    image_data = utils.get_cover(song)
    pixmap = QtGui.QPixmap()

    if image_data is not None:
        pixmap.loadFromData(image_data.read())
        pixmap = pixmap.scaled(
            size, size, mode=QtCore.Qt.TransformationMode.SmoothTransformation
        )

    return pixmap


class SongList(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(150)
        self.setResizeMode(QtWidgets.QListWidget.ResizeMode.Adjust)
        self.setFlow(QtWidgets.QListWidget.Flow.TopToBottom)
        self.setViewMode(QtWidgets.QListWidget.ViewMode.IconMode)

        max_size = QtCore.QSize(0, 0)

        self.song_list: list[SongListItem] = []

        for i in range(20):
            item = SongListItem(self, f"Song {i}")
            self.song_list.append(item)
            self.addItem(item)

            item_size = item.sizeHint()
            max_size.setWidth(max(max_size.width(), item_size.width()))
            max_size.setHeight(max(max_size.height(), item_size.height()))

        for item in self.song_list:
            item.setSizeHint(max_size)


class SongListItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent: QtWidgets.QListWidget, name: str):
        super().__init__(parent)

        self.widget = QtWidgets.QWidget()

        layout = QtWidgets.QHBoxLayout()
        self.widget.setLayout(layout)

        layout.addWidget(
            QtWidgets.QLabel(
                "000",
                alignment=QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignCenter,
            )
        )
        layout.addWidget(QtWidgets.QLabel(name))
        layout.addWidget(
            QtWidgets.QLabel(
                "TEST",
                alignment=QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignCenter,
            )
        )

        self.setSizeHint(self.widget.sizeHint())

        parent.setItemWidget(self, self.widget)


class AlbumWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, album: str) -> None:
        super().__init__(parent=parent)
        self.setFixedHeight(150)

        # Build UI

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.album_cover = QtWidgets.QLabel(text="ALBUM_COVER")
        self.album_cover.setFixedWidth(150)
        self.album_cover.setFixedHeight(150)
        pixmap = QtGui.QPixmap(album)
        pixmap = pixmap.scaled(150, 150)
        self.album_cover.setPixmap(pixmap)
        layout.addWidget(self.album_cover)

        # """
        self.song_list = SongList()

        """
        self.song_list = QtWidgets.QListWidget()
        self.song_list.setFixedHeight(150)
        self.song_list.setResizeMode(QtWidgets.QListWidget.ResizeMode.Adjust)
        # self.song_list.setFlow(QtWidgets.QListWidget.Flow.LeftToRight)
        self.song_list.setViewMode(QtWidgets.QListWidget.ViewMode.IconMode)
        
        for i in range(20):
            item = SongListItem(self.song_list, f"Song {i}")
            self.song_list.addItem(item)
        # """

        layout.addWidget(self.song_list)


root_path = "D:/Music/Zombie Nation"
dirs = [
    "1999 - Leichenschmaus",
    "2003 - Absorber",
    "2006 - Black toys",
    "2009 - Zombielicious",
    "2012 - RGB",
    "2025 - don't exist",
]


app = QtWidgets.QApplication(sys.argv)

mw = QtWidgets.QMainWindow()
mw.setMinimumSize(800, 600)

album_tree = QtWidgets.QTreeWidget()
album_tree.setHeaderHidden(True)
mw.setCentralWidget(album_tree)

for dir in dirs:
    file_path = os.path.join(root_path, dir, "cover.jpg")

    album_item = QtWidgets.QTreeWidgetItem(album_tree)
    album_item.setText(0, dir)
    album_tree.addTopLevelItem(album_item)

    album_content = QtWidgets.QTreeWidgetItem(album_item)
    album_widget = AlbumWidget(album_tree, file_path)
    album_item.addChild(album_content)

    album_tree.setItemWidget(album_content, 0, album_widget)

album_tree.expandAll()


mw.show()

rv = app.exec()

sys.exit(rv)
