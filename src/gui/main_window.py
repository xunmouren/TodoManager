from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QApplication
)
from .sidebar import Sidebar
from .task_list import TaskList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.center_window()

    def setup_window(self):
        self.setWindowTitle("TodoManager")
        self.resize(1000,620)

    def setup_ui(self):
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.sidebar = Sidebar()
        self.task_list = TaskList()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.task_list)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def center_window(self):
        """将窗口中心对准主屏幕中心"""
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        
        # 直接计算窗口左上角位置
        x = screen_rect.center().x() - self.width() // 2
        y = screen_rect.center().y() - self.height() // 2
        
        self.move(x, y)
