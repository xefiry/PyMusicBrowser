from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from ..player import Player


class NavigationWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, player: Player) -> None:
        super().__init__(parent=parent)
        self.player = player

        self.setFixedWidth(200)

        # Build UI

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.search_bar = QtWidgets.QLineEdit()
        layout.addWidget(self.search_bar)

        self.clear_button = QtWidgets.QPushButton("Clear filters")
        self.clear_button.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        layout.addWidget(self.clear_button)

        self.item_list = QtWidgets.QTreeWidget()
        self.item_list.setHeaderHidden(True)
        self.item_list.setColumnCount(1)
        layout.addWidget(self.item_list)

        self.filter_bar = QtWidgets.QLineEdit()
        self.filter_bar.setReadOnly(True)
        layout.addWidget(self.filter_bar)

        for name in ["Album Artist", "Song Artist", "Genre", "Year"]:
            x = QtWidgets.QTreeWidgetItem()
            x.setText(0, name)
            self.item_list.addTopLevelItem(x)

            for j in range(10):
                y = QtWidgets.QTreeWidgetItem()
                y.setText(0, f"item {j:2}")
                x.addChild(y)

        self.do_clear_filter()

        # Connect UI

        self.clear_button.clicked.connect(self.do_clear_filter)
        self.item_list.itemClicked.connect(self.do_select_item)

    def do_clear_filter(self) -> None:
        self.search_bar.setText("")
        self.item_list.setCurrentItem(None)  # type: ignore
        self.filter_bar.setText("<No active filter>")

    def do_select_item(self, item: QtWidgets.QTreeWidgetItem) -> None:
        parent_item = item.parent()
        if parent_item is None:
            return

        self.filter_bar.setText(f"Filter : {parent_item.text(0)} | {item.text(0)}")

    def update_ui(self) -> None:
        pass
