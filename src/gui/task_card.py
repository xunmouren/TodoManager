from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QCheckBox, QPushButton, QInputDialog
from PySide6.QtCore import Signal


class TaskCard(QFrame):
    """
    单个任务卡片
    显示一个任务的标题、完成状态，提供编辑和删除功能
    """

    # 自定义信号
    delete_requested = Signal(object)
    status_changed = Signal(object)
    edit_requested = Signal(object)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        """构建卡片界面"""
        # 设置对象名称，用于 QSS 样式
        self.setObjectName("TaskCard")
        self.setFixedHeight(55)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 10, 5)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)

        self.label = QLabel(self.task.title)

        # 编辑按钮和删除按钮
        self.edit_button = QPushButton("✏️")
        self.delete_button = QPushButton("🗑")

        # 设置对象名称，用于不同的样式（编辑按钮蓝色悬停，删除按钮红色悬停）
        self.edit_button.setObjectName("EditButton")
        self.delete_button.setObjectName("DeleteButton")

        self.edit_button.setFixedSize(35, 35)
        self.delete_button.setFixedSize(35, 35)

        # 将所有组件添加到布局
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.checkbox.stateChanged.connect(self.change_status)
        self.edit_button.clicked.connect(self.edit)
        self.delete_button.clicked.connect(self.delete)
        self.update_style()

    def change_status(self):
        self.task.completed = self.checkbox.isChecked()
        self.update_style()
        self.status_changed.emit(self.task)

    def edit(self):
        """切换任务的完成状态"""
        text, ok = QInputDialog.getText(
            self,
            "编辑任务",
            "任务名称:",
            text=self.task.title
        )
        if ok and text.strip():
            self.task.title = text.strip()
            self.label.setText(self.task.title)
            self.edit_requested.emit(self.task)

    def update_style(self):
        """根据完成状态更新样式"""
        if self.task.completed:
            self.label.setStyleSheet("color:#9ca3af;text-decoration:line-through;")
        else:
            self.label.setStyleSheet("color:#111827;")
    def delete(self):
        """删除任务"""
        self.delete_requested.emit(self)
