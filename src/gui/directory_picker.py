from PySide6 import QtUiTools, QtWidgets
from PySide6.QtWidgets import QWidget


class DirectoryPicker:
    def __init__(self, parent: QWidget, dir_list: list[str]) -> None:
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("src/gui/directory_picker.ui", parent)

        self.dir_list = self.ui.dir_list  # pyright: ignore[reportAttributeAccessIssue]
        self.add_button = self.ui.add_button  # pyright: ignore[reportAttributeAccessIssue]
        self.modify_button = self.ui.modify_button  # pyright: ignore[reportAttributeAccessIssue]
        self.remove_button = self.ui.remove_button  # pyright: ignore[reportAttributeAccessIssue]
        self.buttonBox = self.ui.buttonBox  # pyright: ignore[reportAttributeAccessIssue]

        # Connect UI

        self.dir_list.itemClicked.connect(self.do_enable_buttons)
        self.add_button.clicked.connect(self.do_add_dir)
        self.modify_button.clicked.connect(self.do_modify_dir)
        self.remove_button.clicked.connect(self.do_remove_dir)
        self.buttonBox.accepted.connect(self.ui.accept)  # pyright: ignore[reportAttributeAccessIssue]
        self.buttonBox.rejected.connect(self.ui.reject)  # pyright: ignore[reportAttributeAccessIssue]

        # Function calls

        self.set_dir_list(dir_list)

    def exec(self) -> int:
        return self.ui.exec()  # pyright: ignore[reportAttributeAccessIssue]

    def do_add_dir(self) -> None:
        dialog = QtWidgets.QFileDialog()

        if directory := dialog.getExistingDirectory():
            item = QtWidgets.QListWidgetItem(self.dir_list)
            item.setText(directory)

    def do_modify_dir(self) -> None:
        dialog = QtWidgets.QFileDialog()
        index = self.dir_list.currentRow()
        selected = self.dir_list.item(index)

        if directory := dialog.getExistingDirectory(dir=selected.text()):
            selected.setText(directory)

    def do_remove_dir(self) -> None:
        index = self.dir_list.currentRow()
        self.dir_list.takeItem(index)

    def do_enable_buttons(self) -> None:
        self.modify_button.setEnabled(True)
        self.remove_button.setEnabled(True)

    def set_dir_list(self, dir_list: list[str]) -> None:
        for dir in dir_list:
            item = QtWidgets.QListWidgetItem(self.dir_list)
            item.setText(dir)

    def get_dir_list(self) -> list[str]:
        dir_list = []

        for i in range(self.dir_list.count()):
            dir_list.append(self.dir_list.item(i).text())

        return dir_list
