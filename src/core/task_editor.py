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
from PySide6.QtCore import QDate
from datetime import datetime
from ..gui.animated_combo import AnimatedComboBox

class TaskEditor(QDialog):
    """任务编辑对话框，用于编辑任务的标题、优先级、分类和截止日期"""
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("编辑任务")
        self.setFixedSize(420, 450)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        # 标题
        title_label = QLabel("标题")
        self.title_input = QLineEdit(self.task.title)

        # 优先级
        priority_label = QLabel("优先级")
        self.priority_box = AnimatedComboBox()
        self.priority_box.setEditable(False)
        self.priority_box.setInsertPolicy(QComboBox.NoInsert)
        self.priority_box.addItem("🔴 高优先级", "high")
        self.priority_box.addItem("🟡 中优先级", "medium")
        self.priority_box.addItem("🟢 低优先级", "low")

        index = self.priority_box.findData(self.task.priority)
        if index >= 0:
            self.priority_box.setCurrentIndex(index)

        # 分类
        category_label = QLabel("分类")
        self.category_input = QLineEdit(self.task.category)

        # 日期
        deadline_label = QLabel("截止日期")
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDisplayFormat("yyyy-MM-dd")
        self.deadline_edit.setButtonSymbols(QDateEdit.UpDownArrows)

        if self.task.deadline:
            date = QDate.fromString(self.task.deadline, "yyyy-MM-dd")
            self.deadline_edit.setDate(date)
        else:
            self.deadline_edit.setDate(QDate.currentDate())

        self.error_label = QLabel()
        self.error_label.setObjectName("ErrorLabel")

        # 按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")

        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(priority_label)
        layout.addWidget(self.priority_box)
        layout.addWidget(category_label)
        layout.addWidget(self.category_input)
        layout.addWidget(deadline_label)
        layout.addWidget(self.deadline_edit)
        layout.addWidget(self.error_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)
        cancel_button.clicked.connect(self.reject)

    def save(self):
        try:
            date = self.deadline_edit.date()
            deadline = date.toString("yyyy-MM-dd")
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            self.error_label.setText("⚠ 日期格式错误")
            return

        self.task.title = self.title_input.text().strip()
        self.task.priority = self.priority_box.currentData()
        self.task.category = self.category_input.text().strip()
        self.task.deadline = deadline

        self.accept()
