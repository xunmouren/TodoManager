from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)
from PySide6.QtCore import Signal

from ..core.category import get_category_items


class Sidebar(QWidget):
    """左侧导航栏，提供页面切换和分类筛选功能"""

    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """构建侧边栏界面"""
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)

        # 标题
        title = QLabel("TodoManager")
        title.setObjectName("SidebarTitle")
        self.layout.addWidget(title)

        # 全部任务
        self.all_button = QPushButton("📋 全部任务")
        self.layout.addWidget(self.all_button)

        # 已完成
        self.completed_button = QPushButton("✅ 已完成")
        self.layout.addWidget(self.completed_button)

        # 分类标题
        category_title = QLabel("📂 分类")
        category_title.setObjectName("CategoryTitle")
        self.layout.addWidget(category_title)

        # 动态添加分类按钮
        self.add_category_buttons()

        # 设置
        self.settings_button = QPushButton("⚙ 设置")
        self.settings_button.setObjectName("SettingsButton")
        self.layout.addWidget(self.settings_button)

        self.layout.addStretch()
        self.setLayout(self.layout)

        # 信号连接
        self.all_button.clicked.connect(lambda: self.page_changed.emit("all"))
        self.completed_button.clicked.connect(lambda: self.page_changed.emit("completed"))
        self.settings_button.clicked.connect(lambda: self.page_changed.emit("settings"))

    def add_category_buttons(self):
        """动态添加分类按钮"""
        for key, name in get_category_items():
            button = QPushButton(f"📁 {name}")
            button.setObjectName("CategoryButton")
            button.clicked.connect(lambda checked=False, k=key: self.page_changed.emit(k))
            self.layout.addWidget(button)
