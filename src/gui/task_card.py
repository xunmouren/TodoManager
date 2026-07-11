from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QCheckBox, QPushButton
from PySide6.QtCore import Signal


class TaskCard(QFrame):

    delete_requested = Signal(object)
    status_changed = Signal(object)

    def __init__(self, task):
        super().__init__()

        self.task = task
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("TaskCard")

        layout = QHBoxLayout()

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)

        self.label = QLabel(self.task.title)

        self.delete_button = QPushButton("🗑")
        self.delete_button.setFixedWidth(40)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        self.checkbox.stateChanged.connect(self.change_status)
        self.delete_button.clicked.connect(self.delete)

        self.update_style()

    def change_status(self):
        self.task.completed = self.checkbox.isChecked()
        self.update_style()
        self.status_changed.emit(self.task)

    def update_style(self):
        if self.task.completed:
            self.label.setStyleSheet(
                "text-decoration: line-through; color: gray;"
            )
        else:
            self.label.setStyleSheet(
                "text-decoration: none; color: black;"
            )

    def delete(self):
        self.delete_requested.emit(self)

