from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)
from PySide6.QtGui import (
    QGuiApplication,
    QShortcut,
    QKeySequence,
    QIcon  #  添加
)
from pathlib import Path

from .sidebar import Sidebar
from .task_list import TaskList
from .footer import Footer
from .settings import SettingsPage
from ..core.config import Config


class MainWindow(QMainWindow):
    """应用程序主窗口"""

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.current_theme = "light"
        self.setup_window()
        self.setup_ui()
        self.setup_shortcuts()
        self.center_window()
        self.apply_theme()

    def setup_window(self):
        """设置窗口基本属性"""
        self.setWindowTitle("TodoManager")
        self.resize(1000, 620)
        self.setMinimumSize(900, 600)
        
        #  设置窗口图标
        icon_path = Path(__file__).parent.parent.parent / "icons" / "main.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        else:
            # 尝试其他常见格式
            for ext in [".png", ".svg"]:
                alt_path = Path(__file__).parent.parent.parent / "icons" / f"main{ext}"
                if alt_path.exists():
                    self.setWindowIcon(QIcon(str(alt_path)))
                    break

    def setup_ui(self):
        """构建用户界面"""
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar()
        self.pages = QStackedWidget()
        self.task_list = TaskList()
        self.settings_page = SettingsPage()

        self.pages.addWidget(self.task_list)
        self.pages.addWidget(self.settings_page)

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages)

        content.setLayout(content_layout)
        main_layout.addWidget(content)

        footer = Footer()
        footer.setFixedHeight(36)
        main_layout.addWidget(footer)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.sidebar.page_changed.connect(self.change_page)
        self.settings_page.settings_changed.connect(self.apply_theme)

    def setup_shortcuts(self):
        """设置全局快捷键"""
        settings = self.config.load()
        shortcuts = settings.get("shortcuts", {})

        search_key = shortcuts.get("search", "Ctrl+F")
        add_key = shortcuts.get("add", "Ctrl+N")

        self.search_shortcut = QShortcut(QKeySequence(search_key), self)
        self.search_shortcut.activated.connect(self.open_search)

        self.add_shortcut = QShortcut(QKeySequence(add_key), self)
        self.add_shortcut.activated.connect(self.focus_task_input)

    def open_search(self):
        """打开搜索"""
        self.pages.setCurrentWidget(self.task_list)
        self.task_list.search_button.open_search()

    def focus_task_input(self):
        """聚焦任务输入框"""
        self.pages.setCurrentWidget(self.task_list)
        self.task_list.input.setFocus()

    def apply_theme(self):
        """应用主题"""
        style_dir = Path(__file__).parent.parent.parent / "style"
        
        settings = self.config.load()
        theme = settings.get("theme", "light")
        color = settings.get("color", "#6366f1")
        
        self.current_theme = theme

        qss_parts = []
        
        base_path = style_dir / "base.qss"
        if base_path.exists():
            qss_parts.append(base_path.read_text(encoding="utf-8"))
        
        theme_path = style_dir / f"{theme}.qss"
        if theme_path.exists():
            theme_qss = theme_path.read_text(encoding="utf-8")
            theme_qss = theme_qss.replace("PRIMARY_COLOR", color)
            qss_parts.append(theme_qss)
        
        final_qss = "\n".join(qss_parts)
        self.setStyleSheet(final_qss)

    def change_page(self, page):
        """切换页面"""
        if page == "settings":
            self.pages.setCurrentWidget(self.settings_page)
        else:
            self.pages.setCurrentWidget(self.task_list)
            self.task_list.change_page(page)

    def center_window(self):
        """窗口居中显示"""
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return

        geometry = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(geometry.center())
        self.move(frame.topLeft())

    def reload_shortcuts(self):
        """重新加载快捷键"""
        self.search_shortcut.deleteLater()
        self.add_shortcut.deleteLater()
        self.setup_shortcuts()
