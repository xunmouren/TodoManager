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
from ..core.category import get_category_name


class TaskCard(QFrame):
    """任务卡片组件，显示任务信息并支持交互操作"""

    delete_requested = Signal(object)
    status_changed = Signal(object)
    edit_requested = Signal(object)
    # 🆕 选择状态变化信号
    selection_changed = Signal(object, bool)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.original_title = task.title
        # 🆕 批量选择相关
        self.batch_mode = False
        self.selected = False
        self.setup_ui()

    def setup_ui(self):
        """构建任务卡片界面"""
        self.setObjectName("TaskCard")
        self.setFixedHeight(100)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(5)

        # ===== 第一行：复选框、标题、操作按钮 =====
        top_layout = QHBoxLayout()

        # 🆕 批量选择复选框（默认隐藏）
        self.batch_checkbox = QCheckBox()
        self.batch_checkbox.setVisible(False)
        self.batch_checkbox.setFixedSize(20, 20)
        self.batch_checkbox.stateChanged.connect(self.on_batch_checked)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)

        self.label = QLabel(self.task.title)
        self.label.setTextFormat(Qt.RichText)

        # 编辑删除按钮
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

        # 🆕 批量选择复选框放在最前面
        top_layout.addWidget(self.batch_checkbox)
        top_layout.addWidget(self.checkbox)
        top_layout.addWidget(self.label)
        top_layout.addStretch()
        top_layout.addWidget(self.edit_button)
        top_layout.addWidget(self.delete_button)

        # ===== 第二行：分类、优先级、日期 =====
        info_layout = QHBoxLayout()

        self.category_label = QLabel()
        self.category_label.setObjectName("CategoryLabel")

        self.priority_label = QLabel()
        self.priority_label.setObjectName("PriorityLabel")

        self.date_label = QLabel()

        info_layout.addWidget(self.category_label)
        info_layout.addWidget(self.priority_label)
        info_layout.addStretch()
        info_layout.addWidget(self.date_label)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(info_layout)
        self.setLayout(main_layout)

        # 信号连接
        self.checkbox.stateChanged.connect(self.change_status)
        self.edit_button.clicked.connect(self.edit)
        self.delete_button.clicked.connect(self.delete)

        self.update_info()

    # 🆕 批量选择相关方法
    def set_batch_mode(self, enabled):
        """设置批量模式"""
        self.batch_mode = enabled
        self.batch_checkbox.setVisible(enabled)
        if not enabled:
            self.set_checked(False)
    
    def set_checked(self, checked):
        """设置选中状态"""
        self.selected = checked
        self.batch_checkbox.setChecked(checked)
        # 选中时改变卡片样式
        if checked:
            self.setStyleSheet("""
                #TaskCard {
                    background: #eef2ff;
                    border: 2px solid #6366f1;
                    border-radius: 16px;
                    padding: 10px;
                }
            """)
        else:
            self.setStyleSheet("")
    
    def is_checked(self):
        """获取选中状态"""
        return self.selected
    
    def on_batch_checked(self, state):
        """批量复选框状态变化"""
        self.selected = state == Qt.Checked
        if self.selected:
            self.setStyleSheet("""
                #TaskCard {
                    background: #eef2ff;
                    border: 2px solid #6366f1;
                    border-radius: 16px;
                    padding: 10px;
                }
            """)
        else:
            self.setStyleSheet("")
        self.selection_changed.emit(self, self.selected)

    def update_info(self):
        """更新分类、优先级、日期信息"""
        category_name = get_category_name(self.task.category)
        self.category_label.setText(f"📁 {category_name}")

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
