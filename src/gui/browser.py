from PySide6 import QtWidgets

from ..player import Player


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

        layout.addWidget(QtWidgets.QTextEdit())

        # Connect UI

        # ...

        # Status member variables

        # ...

    def update_ui(self) -> None:
        pass
