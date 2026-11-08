from PySide6 import QtCore, QtGui

from ..database import utils
from ..database.song import Song


def s_to_t(seconds: float) -> str:
    """Convert a number of seconds to displayable time"""
    result: str = ""

    h = seconds // 3600
    seconds = seconds % 3600

    s = int(seconds % 60)
    m = int(seconds // 60)

    if h > 0:
        result = f"{h}:{m:02}:{s:02}"
    else:
        result = f"{m}:{s:02}"

    return result


def get_cover(song: Song, size: int) -> QtGui.QPixmap:
    image_data = utils.get_cover(str(song.file_path))
    pixmap = QtGui.QPixmap()

    if image_data is not None:
        pixmap.loadFromData(image_data.read())
        pixmap = pixmap.scaled(
            size, size, mode=QtCore.Qt.TransformationMode.SmoothTransformation
        )

    return pixmap
