from PySide6 import QtCore, QtGui, QtUiTools
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

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


def load_widget_from_file[TWidget: QWidget](
    path: str, widget_type: type[TWidget], parent: QWidget | None = None
) -> TWidget:
    """Load Qt widget from file.

    Raises:
        TypeError: If the loaded widget is not of the expected type.
    """
    loader = QtUiTools.QUiLoader()
    result = loader.load(path, parent)

    if not isinstance(result, widget_type):
        raise TypeError(f"{path} is not a {widget_type.__name__}")

    return result


def get_child[TObject: QObject](
    widget: QWidget, child_type: type[TObject], child_name: str
) -> TObject:
    """Get child of widget.

    Raises:
        RuntimeError: If the child is not found.
    """
    result = widget.findChild(child_type, child_name)
    if result is None:
        raise RuntimeError(
            f"Could not find widget {child_name} ({child_type.__name__}) in {widget}"
        )

    return result
