from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QCheckBox, QPushButton, QInputDialog
from PySide6.QtCore import Signal


class TaskCard(QFrame):

    delete_requested = Signal(object)
    status_changed = Signal(object)
    edit_requested = Signal(object)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("TaskCard")
        self.setFixedHeight(55)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 10, 5)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)

        self.label = QLabel(self.task.title)

        self.edit_button = QPushButton("✏️")
        self.delete_button = QPushButton("🗑")

        self.edit_button.setObjectName("EditButton")
        self.delete_button.setObjectName("DeleteButton")

        self.edit_button.setFixedSize(35, 35)
        self.delete_button.setFixedSize(35, 35)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.checkbox.stateChanged.connect(self.change_status)
        self.edit_button.clicked.connect(self.edit)
        self.delete_button.clicked.connect(self.delete)
        self.update_style()

    def change_status(self):
        self.task.completed = self.checkbox.isChecked()
        self.update_style()
        self.status_changed.emit(self.task)

    def edit(self):
        text, ok = QInputDialog.getText(
            self,
            "编辑任务",
            "任务名称:",
            text=self.task.title
        )
        if ok and text.strip():
            self.task.title = text.strip()
            self.label.setText(self.task.title)
            self.edit_requested.emit(self.task)

    def update_style(self):
        if self.task.completed:
            self.label.setStyleSheet("color:#9ca3af;text-decoration:line-through;")
        else:
            self.label.setStyleSheet("color:#111827;")
    def delete(self):
        self.delete_requested.emit(self)
