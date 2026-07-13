from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton
)
from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtGui import QIcon

from ..core.task_editor import TaskEditor


class TaskCard(QFrame):
    """任务卡片组件，显示单个任务信息并支持交互操作"""

    delete_requested = Signal(object)
    status_changed = Signal(object)
    edit_requested = Signal(object)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.original_title = task.title
        self.setup_ui()

    def setup_ui(self):
        """构建UI组件"""
        self.setObjectName("TaskCard")
        self.setFixedHeight(90)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(5)

        # ===== 第一行：复选框、标题、操作按钮 =====
        top_layout = QHBoxLayout()

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)

        self.label = QLabel(self.task.title)
        self.label.setTextFormat(Qt.RichText)  # 支持搜索高亮HTML

        # 图标按钮
        self.edit_button = QPushButton()
        self.delete_button = QPushButton()
        self.edit_button.setIcon(QIcon("./icons/edit.svg"))
        self.delete_button.setIcon(QIcon("./icons/delete.svg"))
        self.edit_button.setIconSize(QSize(18, 18))
        self.delete_button.setIconSize(QSize(18, 18))

        self.edit_button.setObjectName("EditButton")
        self.delete_button.setObjectName("DeleteButton")
        self.edit_button.setFixedSize(40, 40)
        self.delete_button.setFixedSize(40, 40)

        top_layout.addWidget(self.checkbox)
        top_layout.addWidget(self.label)
        top_layout.addStretch()
        top_layout.addWidget(self.edit_button)
        top_layout.addWidget(self.delete_button)

        # ===== 第二行：优先级、日期 =====
        info_layout = QHBoxLayout()
        self.priority_label = QLabel()
        self.date_label = QLabel()

        info_layout.addWidget(self.priority_label)
        info_layout.addStretch()
        info_layout.addWidget(self.date_label)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(info_layout)
        self.setLayout(main_layout)

        # 连接信号
        self.checkbox.stateChanged.connect(self.change_status)
        self.edit_button.clicked.connect(self.edit)
        self.delete_button.clicked.connect(self.delete)

        self.update_info()

    def update_info(self):
        """更新优先级和日期信息"""
        priority_map = {
            "high": ("🔴 高优先级", "#ef4444"),
            "medium": ("🟡 中优先级", "#eab308"),
            "low": ("🟢 低优先级", "#22c55e")
        }
        text, color = priority_map.get(
            self.task.priority,
            ("🟡 中优先级", "#eab308")
        )

        self.priority_label.setText(text)
        self.priority_label.setStyleSheet(
            f"""
            color:{color};
            font-weight:bold;
            """
        )

        if self.task.deadline:
            self.date_label.setText(f"📅 {self.task.deadline}")
        else:
            self.date_label.setText("")

    # ===== 搜索高亮 =====
    def highlight(self, keyword):
        """根据关键词高亮标题文本"""
        if not keyword:
            self.label.setText(self.original_title)
            return

        title = self.original_title
        lower_title = title.lower()
        lower_key = keyword.lower()

        if lower_key in lower_title:
            start = lower_title.index(lower_key)
            end = start + len(keyword)

            result = (
                title[:start]
                + "<span style='background:#fde68a;color:#111827;'>"
                + title[start:end]
                + "</span>"
                + title[end:]
            )
            self.label.setText(result)
        else:
            self.label.setText(title)

    def change_status(self):
        """切换任务完成状态"""
        self.task.completed = self.checkbox.isChecked()
        self.status_changed.emit(self.task)

    def edit(self):
        """编辑任务"""
        dialog = TaskEditor(self.task, self)
        if dialog.exec():
            self.original_title = self.task.title
            self.label.setText(self.task.title)
            self.update_info()
            self.edit_requested.emit(self.task)

    def delete(self):
        """删除任务"""
        self.delete_requested.emit(self)
