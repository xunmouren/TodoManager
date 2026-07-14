from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QColorDialog,
    QKeySequenceEdit,
    QMessageBox
)

from ..core.config import Config
from ..core.manager import TaskManager
from PySide6.QtCore import Signal


class SettingsPage(QWidget):
    """设置页面，管理应用配置和快捷键"""
    settings_changed = Signal()

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.manager = TaskManager()
        self.color = "#6366f1"
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """构建设置界面"""
        layout = QVBoxLayout()

        title = QLabel("⚙ 设置")
        title.setObjectName("PageTitle")

        # 主题
        theme_label = QLabel("主题")
        self.theme_box = QComboBox()
        self.theme_box.addItem("浅色", "light")
        self.theme_box.addItem("深色", "dark")

        # 自定义颜色
        color_label = QLabel("主题颜色")
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.choose_color)

        # 字体大小
        font_label = QLabel("字体大小")
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 30)

        # 快捷键
        shortcut_label = QLabel("快捷键")
        search_label = QLabel("搜索任务")
        self.search_shortcut = QKeySequenceEdit()

        add_label = QLabel("添加任务")
        self.add_shortcut = QKeySequenceEdit()

        # 清空任务
        clear_button = QPushButton("🗑 清空所有任务")
        clear_button.clicked.connect(self.clear_tasks)

        # 保存按钮
        save = QPushButton("保存设置")
        save.clicked.connect(self.save_settings)

        # 按顺序添加所有控件
        for w in [
            title, theme_label, self.theme_box,
            color_label, self.color_button,
            font_label, self.font_size,
            shortcut_label,
            search_label, self.search_shortcut,
            add_label, self.add_shortcut,
            clear_button, save
        ]:
            layout.addWidget(w)

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
                """
            )

    def load_settings(self):
        """加载配置到界面"""
        data = self.config.load()

        # 主题
        index = self.theme_box.findData(data["theme"])
        if index >= 0:
            self.theme_box.setCurrentIndex(index)

        # 字体大小
        self.font_size.setValue(data["font_size"])

        # 颜色
        self.color = data.get("color", "#6366f1")
        self.color_button.setStyleSheet(
            f"""
            background:{self.color};
            color:white;
            """
        )

        # 快捷键
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
                "search":self.search_shortcut.keySequence().toString() or "Ctrl+F",
                "add": self.add_shortcut.keySequence().toString() or "Ctrl+N"
            }
        }
        self.config.save(data)
        self.settings_changed.emit()

    def clear_tasks(self):
        """清空所有任务"""
        result = QMessageBox.warning(
            self,
            "确认",
            "确定删除所有任务吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:
            self.manager.clear_tasks()
            QMessageBox.information(self, "完成", "任务已经全部清空")
    
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
