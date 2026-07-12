from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QPoint
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
        self.drag_position = QPoint()
        self.setup_window()
        self.setup_ui()
        self.center_window()

    def setup_window(self):
        """设置窗口的基本属性"""
        self.setWindowTitle("TodoManager")
        self.resize(1000, 620)
        # 设置窗口为无边框（才能实现圆角）
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 启用透明背景（圆角才能显示）
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setup_ui(self):
        """构建用户界面"""
        # 创建一个容器组件，作为中央部件
        container = QWidget()
        # 给容器设置圆角样式
        container.setObjectName("MainContainer")

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
    
    def mousePressEvent(self, event):
        """鼠标按下时记录位置"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动时拖动窗口"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放时清空拖动位置"""
        self.drag_position = QPoint()

