from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton
)
from PySide6.QtCore import Signal
from src.core.task_editor import TaskEditor


class TaskCard(QFrame):
    """
    任务卡片组件，显示单个任务的信息并支持交互操作。
    
    Attributes:
        delete_requested: 删除任务信号
        status_changed: 状态变更信号
        edit_requested: 编辑任务信号
    """

    delete_requested = Signal(object)
    status_changed = Signal(object)
    edit_requested = Signal(object)

    def __init__(self, task):
        """
        初始化任务卡片。
        
        Args:
            task: 任务对象
        """
        super().__init__()
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        """初始化UI组件。"""
        self.setObjectName("TaskCard")
        self.setFixedHeight(90)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(5)

        # 第一行：复选框、标题、操作按钮
        top_layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)
        self.label = QLabel(self.task.title)
        self.edit_button = QPushButton("✏️")
        self.delete_button = QPushButton("🗑")

        # 保留QSS选择器
        self.edit_button.setObjectName("EditButton")
        self.delete_button.setObjectName("DeleteButton")
        self.edit_button.setFixedSize(40, 40)
        self.delete_button.setFixedSize(40, 40)

        top_layout.addWidget(self.checkbox)
        top_layout.addWidget(self.label)
        top_layout.addStretch()
        top_layout.addWidget(self.edit_button)
        top_layout.addWidget(self.delete_button)

        # 第二行信息：优先级标签、日期标签
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
        """更新优先级和日期信息。"""
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

    def change_status(self):
        """切换任务完成状态。"""
        self.task.completed = self.checkbox.isChecked()
        self.status_changed.emit(self.task)

    def edit(self):
        """编辑任务。"""
        dialog = TaskEditor(self.task, self)
        if dialog.exec():
            self.label.setText(self.task.title)
            self.update_info()
            self.edit_requested.emit(self.task)

    def delete(self):
        """删除任务。"""
        self.delete_requested.emit(self)
