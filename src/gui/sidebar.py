from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)
from PySide6.QtCore import Signal


class Sidebar(QWidget):
    """
    左侧导航侧边栏，提供页面切换功能

    Signals:
        page_changed: 页面切换信号，参数为页面标识（all/completed/settings）
    """

    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """构建侧边栏界面"""
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout()

        # 标题
        title = QLabel("TodoManager")
        title.setObjectName("SidebarTitle")
        layout.addWidget(title)

        # 任务页面按钮
        self.all_button = QPushButton("📋 全部任务")
        self.completed_button = QPushButton("✅ 已完成")
        layout.addWidget(self.all_button)
        layout.addWidget(self.completed_button)

        # 设置按钮
        self.settings_button = QPushButton("⚙ 设置")
        self.settings_button.setObjectName("SettingsButton")
        layout.addWidget(self.settings_button)

        layout.addStretch()
        self.setLayout(layout)

        # 信号连接
        self.all_button.clicked.connect(lambda: self.page_changed.emit("all"))
        self.completed_button.clicked.connect(lambda: self.page_changed.emit("completed"))
        self.settings_button.clicked.connect(lambda: self.page_changed.emit("settings"))
