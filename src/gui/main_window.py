from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QGuiApplication
from .sidebar import Sidebar
from .task_list import TaskList


class MainWindow(QMainWindow):
    """
    应用程序主窗口
    继承自 QMainWindow 提供菜单栏、工具栏、状态栏等高级功能
    """
    def __init__(self):
        # 调用父类构造函数
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.center_window()

    def setup_window(self):
        """设置窗口的基本属性"""
        self.setWindowTitle("TodoManager")
        self.resize(1000, 620)

    def setup_ui(self):
        """构建用户界面"""
        # 创建一个容器组件，作为中央部件
        container = QWidget()

        # 创建水平布局，让侧边栏和任务列表左右排列
        layout = QHBoxLayout()
        # 将布局的外边距设为0，让组件紧贴窗口边缘
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建侧边栏和任务列表实例
        self.sidebar = Sidebar()
        self.task_list = TaskList()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.task_list)

        container.setLayout(layout)
        self.setCentralWidget(container)
        # 当用户点击"全部任务"或"已完成"时，任务列表会相应刷新
        self.sidebar.page_changed.connect(self.task_list.change_page)
    
    def center_window(self):
        """将窗口中心对准主屏幕中心"""
        # 主屏幕
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())