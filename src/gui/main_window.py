from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
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

        # 创建垂直布局（内容在上，底部信息在下）
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== 内容区域（侧边栏 + 任务列表） =====
        content = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # 创建侧边栏和任务列表实例
        self.sidebar = Sidebar()
        self.task_list = TaskList()

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.task_list)

        content.setLayout(content_layout)

        # ===== 底部信息栏（GitHub + 版权） =====
        footer = QWidget()
        footer.setObjectName("Footer")
        footer.setFixedHeight(36)
        
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(20, 0, 20, 0)

        # GitHub 超链接（左下角）
        self.github_label = QLabel()
        self.github_label.setObjectName("GitHubLabel")
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setText(
            '<a href="https://github.com/xunmouren/TodoManager.git" style="color: #6b7280; font-size: 13px; text-decoration: none; font-weight: 500;">'
            '📦GitHub'
            '</a>'
        )

        # 版权信息（右下角）
        self.copyright_label = QLabel("© 2026 TodoManager")
        self.copyright_label.setObjectName("CopyrightLabel")
        self.copyright_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        footer_layout.addWidget(self.github_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.copyright_label)

        footer.setLayout(footer_layout)

        # 组装：内容 + 底部
        main_layout.addWidget(content)  # 内容区域（拉伸填满）
        main_layout.addWidget(footer)   # 底部（固定高度）

        container.setLayout(main_layout)
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
