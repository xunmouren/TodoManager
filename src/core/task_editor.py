from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QDateEdit
)
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDate
from datetime import datetime

from ..gui.animated_combo import AnimatedComboBox


class TaskEditor(QDialog):
    """任务编辑对话框，编辑标题、优先级、分类、截止日期"""

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        """构建编辑对话框界面"""
        self.setWindowTitle("编辑任务")
        self.setFixedSize(420, 420)  # 增加高度，避免按钮被裁剪
        self.setObjectName("TaskEditor")

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        # ===== 标题 =====
        title_label = QLabel("标题")
        self.title_input = QLineEdit(
            self.task.title if hasattr(self.task, "title") else ""
        )

        # ===== 优先级 =====
        priority_label = QLabel("优先级")
        self.priority_box = AnimatedComboBox()
        self.priority_box.setEditable(False)
        self.priority_box.setInsertPolicy(QComboBox.NoInsert)

        self.priority_box.addItem("🔴 高优先级", "high")
        self.priority_box.addItem("🟡 中优先级", "medium")
        self.priority_box.addItem("🟢 低优先级", "low")

        if hasattr(self.task, "priority"):
            index = self.priority_box.findData(self.task.priority)
            if index >= 0:
                self.priority_box.setCurrentIndex(index)

        # ===== 分类 =====
        category_label = QLabel("分类")
        self.category_input = QLineEdit(
            self.task.category if hasattr(self.task, "category") else ""
        )

        # ===== 截止日期 =====
        deadline_label = QLabel("截止日期")
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)  # 开启日历弹窗
        self.deadline_edit.setDisplayFormat("yyyy-MM-dd")  # 显示格式
        self.deadline_edit.setDate(QDate.currentDate())  # 默认今天

        # 加载已有日期
        if hasattr(self.task, "deadline") and self.task.deadline:
            try:
                date = QDate.fromString(self.task.deadline, "yyyy-MM-dd")
                if date.isValid():
                    self.deadline_edit.setDate(date)
            except Exception:
                self.deadline_edit.setDate(QDate.currentDate())

        # ===== 错误提示 =====
        self.error_label = QLabel()
        self.error_label.setObjectName("ErrorLabel")

        # ===== 按钮 =====
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        save_button = QPushButton("保存")
        save_button.setObjectName("SaveButton")

        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("CancelButton")

        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # ===== 主布局 =====
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(priority_label)
        layout.addWidget(self.priority_box)
        layout.addWidget(category_label)
        layout.addWidget(self.category_input)
        layout.addWidget(deadline_label)
        layout.addWidget(self.deadline_edit)
        layout.addWidget(self.error_label)
        layout.addStretch()  # 自动占据剩余空间
        button_widget = QWidget()  # noqa: F821
        button_widget.setFixedHeight(50)

        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        self.setLayout(layout)

        # ===== 信号 =====
        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)

    def save(self):
        """保存任务数据并进行验证"""
        # 标题验证
        title = self.title_input.text().strip()
        if not title:
            self.error_label.setText("⚠ 请输入任务标题")
            return

        # 日期验证
        try:
            date = self.deadline_edit.date()
            deadline = date.toString("yyyy-MM-dd")
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            self.error_label.setText("⚠ 日期格式错误")
            return

        # 保存任务
        self.task.title = self.title_input.text().strip()
        self.task.priority = self.priority_box.currentData()
        self.task.category = self.category_input.text().strip()
        self.task.deadline = deadline

        self.accept()