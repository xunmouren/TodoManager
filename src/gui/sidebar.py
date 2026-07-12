from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    """
    左侧导航侧边栏
    提供页面切换功能
    """
    # 自定义信号：当用户切换页面时发射，携带页面标识字符串
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """构建侧边栏界面"""
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        layout = QVBoxLayout()
        title = QLabel("TodoManager")
        # 用于样式美化
        title.setObjectName("SidebarTitle")

        # 创建导航按钮
        self.all_button = QPushButton("📋 全部任务")
        self.completed_button = QPushButton("✅ 已完成")

        # 将组件添加到布局中
        layout.addWidget(title)
        layout.addWidget(self.all_button)
        layout.addWidget(self.completed_button)
        layout.addStretch()

        self.setLayout(layout)
        # 连接按钮点击事件到信号发射
        self.all_button.clicked.connect(lambda: self.page_changed.emit("all"))
        self.completed_button.clicked.connect(lambda: self.page_changed.emit("completed"))
