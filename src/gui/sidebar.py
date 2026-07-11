from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    page_changed = Signal(str)
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        layout = QVBoxLayout()
        title = QLabel("TodoManager")
        title.setObjectName("SidebarTitle")

        self.all_button = QPushButton("📋 全部任务")
        self.completed_button = QPushButton("✅ 已完成")

        layout.addWidget(title)
        layout.addWidget(self.all_button)
        layout.addWidget(self.completed_button)
        layout.addStretch()

        self.setLayout(layout)
        self.all_button.clicked.connect(lambda: self.page_changed.emit("all"))
        self.completed_button.clicked.connect(lambda: self.page_changed.emit("completed"))
