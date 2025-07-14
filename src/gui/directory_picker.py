from PySide6 import QtWidgets, QtCore


class DirectoryPicker(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, dir_list: list[str]) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("List of directories to scan for music")
        self.setFixedSize(500, 200)

        # Build UI

        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)

        self.dir_list = QtWidgets.QListWidget()
        _mode = QtWidgets.QAbstractItemView.DragDropMode.InternalMove
        self.dir_list.setDragDropMode(_mode)
        layout.addWidget(self.dir_list)

        buttons_widget = QtWidgets.QWidget()
        layout.addWidget(buttons_widget)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        buttons_widget.setLayout(buttons_layout)

        self.add_button = QtWidgets.QPushButton("Add")
        buttons_layout.addWidget(self.add_button)

        self.modify_button = QtWidgets.QPushButton("Modify")
        self.modify_button.setEnabled(False)
        buttons_layout.addWidget(self.modify_button)

        self.remove_button = QtWidgets.QPushButton("Remove")
        self.remove_button.setEnabled(False)
        buttons_layout.addWidget(self.remove_button)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        layout.addWidget(self.buttonBox)

        # Connect UI

        self.dir_list.itemClicked.connect(self.do_enable_buttons)
        self.add_button.clicked.connect(self.do_add_dir)
        self.modify_button.clicked.connect(self.do_modify_dir)
        self.remove_button.clicked.connect(self.do_remove_dir)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Function calls

        self.set_dir_list(dir_list)

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
        # if list is empty, do nothing
        if len(dir_list) == 0:
            return

        for dir in dir_list:
            item = QtWidgets.QListWidgetItem(self.dir_list)
            item.setText(dir)

    def get_dir_list(self) -> list[str]:
        dir_list = []

        for i in range(self.dir_list.count()):
            dir_list.append(self.dir_list.item(i).text())

        return dir_list
