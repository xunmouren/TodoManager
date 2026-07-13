from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PySide6.QtGui import QGuiApplication
from .sidebar import Sidebar
from .task_list import TaskList
from .footer import Footer


class MainWindow(QMainWindow):
    """应用程序主窗口"""

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.center_window()

    def setup_window(self):
        """设置窗口基本属性"""
        self.setWindowTitle("TodoManager")
        self.resize(1000, 620)

    def setup_ui(self):
        """构建用户界面"""
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 内容区域 侧边栏 + 任务列表
        content = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar()
        self.task_list = TaskList()

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.task_list)

        content.setLayout(content_layout)
        main_layout.addWidget(content)

        # 底部信息栏
        footer = Footer()
        footer.setFixedHeight(36)
        main_layout.addWidget(footer)

        # 页面切换信号
        self.sidebar.page_changed.connect(self.task_list.change_page)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def center_window(self):
        """窗口居中显示"""
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return

        geometry = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(geometry.center())
        self.move(frame.topLeft())
