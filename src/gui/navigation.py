from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from ..player import Player
from .. import database

# TODO merge with browser to be able to access these fields from browser


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
        self.search_bar.setPlaceholderText("Search filters ...")
        self.search_bar.setClearButtonEnabled(True)
        layout.addWidget(self.search_bar)

        self.clear_button = QtWidgets.QPushButton("Clear filters")
        self.clear_button.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        layout.addWidget(self.clear_button)

        self.filter_bar = QtWidgets.QLineEdit()
        self.filter_bar.setPlaceholderText("<No active filter>")
        self.filter_bar.setReadOnly(True)
        layout.addWidget(self.filter_bar)

        self.item_list = QtWidgets.QTreeWidget()
        self.item_list.setHeaderHidden(True)
        self.item_list.setColumnCount(1)
        layout.addWidget(self.item_list)

        # Connect UI

        self.search_bar.textChanged.connect(self.do_search)
        self.clear_button.clicked.connect(self.do_clear_filter)
        self.item_list.itemClicked.connect(self.do_select_item)

        # Function calls

        self.update_data()

    def update_data(self) -> None:
        self.item_list.clear()

        for name, items in [
            ("Album Artist", database.get_artists(has_album=True)),
            ("Song Artist", database.get_artists(has_song=True)),
            ("Genre", database.get_genres()),
            ("Year", database.get_years()),  # TODO filter by decade and not by year
        ]:
            category = QtWidgets.QTreeWidgetItem()
            category.setText(0, name)
            self.item_list.addTopLevelItem(category)

            for item in items:
                filter = QtWidgets.QTreeWidgetItem()
                filter.setText(0, str(item))
                category.addChild(filter)

        self.do_clear_filter()

    def do_search(self, input: str) -> None:
        hide_category: bool
        hide_filter: bool

        root = self.item_list.invisibleRootItem()

        for i in range(root.childCount()):
            category = root.child(i)

            hide_category = True

            for j in range(category.childCount()):
                filter = category.child(j)

                # ToDo: ignore accentuated characters
                hide_filter = input.lower() not in filter.text(0).lower()

                filter.setHidden(hide_filter)

                # don't hide category if we show (not hidden) at least one filter
                hide_category = hide_category and hide_filter

            # expand filter section if input is not empty and filter is not hidden
            category.setExpanded(input != "" and not hide_category)

            category.setHidden(hide_category)

    def do_clear_filter(self) -> None:
        self.search_bar.clear()
        self.item_list.setCurrentItem(None)  # type: ignore
        self.filter_bar.clear()

    def do_select_item(self, item: QtWidgets.QTreeWidgetItem) -> None:
        parent_item = item.parent()
        if parent_item is None:
            return

        self.filter_bar.setText(f"{parent_item.text(0)} | {item.text(0)}")
