from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton
)
from PySide6.QtCore import Signal

class TaskCard(QFrame):
    # 删除信号
    delete_requested = Signal(object)
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("TaskCard")
        layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.label = QLabel(self.title)
        self.delete_button = QPushButton("🗑")
        self.delete_button.setFixedWidth(40)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.delete_button)
        self.setLayout(layout)
        # 信号
        self.checkbox.stateChanged.connect(self.toggle_complete)
        self.delete_button.clicked.connect(self.delete_task)

    def toggle_complete(self):
        if self.checkbox.isChecked():
            self.label.setStyleSheet(
                """
                text-decoration: line-through;
                color: gray;
                """
            )
        else:
            self.label.setStyleSheet(
                """
                text-decoration:none;
                color:black;
                """
            )

    def delete_task(self):
        self.delete_requested.emit(self)
