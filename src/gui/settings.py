from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QColorDialog,
    QKeySequenceEdit,
    QMessageBox,
    QHBoxLayout
)
from PySide6.QtCore import Signal

from ..core.config import Config
from ..core.manager import TaskManager


class SettingsPage(QWidget):
    """设置页面，管理应用配置"""

    settings_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("SettingsPage")
        self.config = Config()
        self.manager = TaskManager()
        self.color = "#6366f1"
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """构建设置界面"""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("⚙ 设置")
        title.setObjectName("PageTitle")

        # 主题切换
        theme_label = QLabel("🌓 主题")
        self.theme_box = QComboBox()
        self.theme_box.addItem("☀️ 亮色", "light")
        self.theme_box.addItem("🌙 暗色", "dark")

        # 颜色
        color_label = QLabel("🎨 主题颜色")
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.choose_color)

        # 字体大小
        font_label = QLabel("📏 字体大小")
        font_layout = QHBoxLayout()
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 30)
        self.font_size.setFixedWidth(80)
        font_layout.addWidget(self.font_size)
        font_layout.addStretch()

        # 快捷键
        shortcut_label = QLabel("⌨️ 快捷键")
        search_label = QLabel("搜索任务")
        self.search_shortcut = QKeySequenceEdit()
        self.search_shortcut.setFixedHeight(32)

        add_label = QLabel("添加任务")
        self.add_shortcut = QKeySequenceEdit()
        self.add_shortcut.setFixedHeight(32)

        # 清空任务
        clear_button = QPushButton("🗑 清空所有任务")
        clear_button.clicked.connect(self.clear_tasks)

        # 保存
        save_button = QPushButton("💾 保存设置")
        save_button.clicked.connect(self.save_settings)

        # 添加所有控件
        layout.addWidget(title)
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_box)
        layout.addWidget(color_label)
        layout.addWidget(self.color_button)
        layout.addWidget(font_label)
        layout.addLayout(font_layout)
        layout.addWidget(shortcut_label)
        layout.addWidget(search_label)
        layout.addWidget(self.search_shortcut)
        layout.addWidget(add_label)
        layout.addWidget(self.add_shortcut)
        layout.addWidget(clear_button)
        layout.addWidget(save_button)

        layout.addStretch()
        self.setLayout(layout)

    def choose_color(self):
        """选择主题颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.color_button.setStyleSheet(
                f"""
                background:{self.color};
                color:white;
                border-radius:8px;
                """
            )

    def load_settings(self):
        """加载配置到界面"""
        data = self.config.load()

        index = self.theme_box.findData(data.get("theme", "light"))
        if index >= 0:
            self.theme_box.setCurrentIndex(index)

        self.font_size.setValue(data.get("font_size", 14))

        self.color = data.get("color", "#6366f1")
        self.color_button.setStyleSheet(
            f"""
            background:{self.color};
            color:white;
            border-radius:8px;
            """
        )

        shortcuts = data.get("shortcuts", {})
        self.search_shortcut.setKeySequence(shortcuts.get("search", "Ctrl+F"))
        self.add_shortcut.setKeySequence(shortcuts.get("add", "Ctrl+N"))

    def save_settings(self):
        """保存界面配置到文件"""
        data = {
            "theme": self.theme_box.currentData(),
            "color": self.color,
            "font_size": self.font_size.value(),
            "shortcuts": {
                "search": self.search_shortcut.keySequence().toString() or "Ctrl+F",
                "add": self.add_shortcut.keySequence().toString() or "Ctrl+N"
            }
        }

        self.config.save(data)
        self.settings_changed.emit()
    
    def clear_tasks(self):
        """清空所有任务"""
        msg = QMessageBox(self)
        msg.setWindowTitle("确认")
        msg.setText("确定删除所有任务吗？")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("是")
        msg.button(QMessageBox.No).setText("否")

        if msg.exec() == QMessageBox.Yes:
            self.manager.clear_tasks()
            QMessageBox.information(self, "完成", "任务已经全部清空")

    # ✅ 移除弹窗，静默保存
    # def save_settings(self):
    #     """保存界面配置到文件"""
    #     data = {
    #         "theme": self.theme_box.currentData(),
    #         "color": self.color,
    #         "font_size": self.font_size.value(),
    #         "shortcuts": {
    #             "search": self.search_shortcut.keySequence().toString() or "Ctrl+F",
    #             "add": self.add_shortcut.keySequence().toString() or "Ctrl+N"
    #         }
    #     }
    #     self.config.save(data)
    #     self.settings_changed.emit()
    #     # ✅ 移除弹窗，直接关闭设置页面
    #     # 返回到任务列表页面
    #     parent = self.parent()
    #     while parent and not hasattr(parent, 'change_page'):
    #         parent = parent.parent()
    #     if parent and hasattr(parent, 'change_page'):
    #         parent.change_page("all")

    # 用中文会出bug，点了没反应
    # def clear_tasks(self):
    #     """清空所有任务"""
    #     msg = QMessageBox(self)
    #     msg.setWindowTitle("确认")
    #     msg.setText("确定删除所有任务吗？")
    #     msg.setIcon(QMessageBox.Warning)

    #     # 创建中文按钮
    #     yes_button = msg.addButton("是", QMessageBox.YesRole)
    #     no_button = msg.addButton("否", QMessageBox.NoRole)

    #     msg.exec()

    #     if msg.clickedButton() == yes_button:
    #         self.manager.clear_tasks()
    #         QMessageBox.information(self, "完成", "任务已经全部清空")
