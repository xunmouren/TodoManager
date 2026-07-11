from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QGuiApplication
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
        self.resize(1000, 620)

    def setup_ui(self):
        container = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar()
        self.task_list = TaskList()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.task_list)

        container.setLayout(layout)
        self.setCentralWidget(container)
        self.sidebar.page_changed.connect(self.task_list.change_page)
    
    def center_window(self):
        # 主屏幕
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
