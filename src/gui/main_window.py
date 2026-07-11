from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
)

from .sidebar import Sidebar
from .task_list import TaskList



class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setup_window()

        self.setup_ui()



    def setup_window(self):

        self.setWindowTitle(
            "TodoManager"
        )

        self.resize(
            1100,
            700
        )



    def setup_ui(self):

        container = QWidget()

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        self.sidebar = Sidebar()

        self.task_list = TaskList()


        layout.addWidget(
            self.sidebar
        )


        layout.addWidget(
            self.task_list
        )


        container.setLayout(
            layout
        )


        self.setCentralWidget(
            container
        )