from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QMessageBox
)
from PySide6.QtCore import Qt

from ..core.manager import TaskManager
from .task_card import TaskCard
from .search_button import SearchButton


class TaskList(QWidget):
    """任务列表主界面，负责显示、添加、删除和管理任务卡片"""

    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.cards = []
        self.tasks = []
        self.current_page = "all"
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """构建界面布局"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)  # 缩小边距，避免溢出
        layout.setSpacing(10)

        # ===== 标题 =====
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("我的任务")
        title.setObjectName("PageTitle")

        header_layout.addWidget(title)
        header_layout.addStretch()

        self.search_button = SearchButton()
        header_layout.addWidget(self.search_button)

        header.setLayout(header_layout)

        # ===== 输入框 =====
        self.input = QLineEdit()
        self.input.setPlaceholderText("输入任务...")

        # ===== 按钮区域 =====
        self.add_button = QPushButton("+ 添加任务")
        self.add_button.setObjectName("AddButton")

        self.clear_button = QPushButton("🗑 清空任务")
        self.clear_button.setObjectName("ClearButton")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)

        # ===== 任务区域 =====
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_layout.setSpacing(2)
        self.task_layout.setContentsMargins(10, 10, 10, 10)
        self.task_layout.setAlignment(Qt.AlignTop)
        self.task_container.setLayout(self.task_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)  # 不固定高度
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.task_container)

        layout.addWidget(header)
        layout.addWidget(self.input)
        layout.addLayout(button_layout)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

        # 信号连接
        self.add_button.clicked.connect(self.add_task)
        self.clear_button.clicked.connect(self.clear_tasks)
        self.input.returnPressed.connect(self.add_task)
        self.search_button.search_changed.connect(self.search)

    def refresh(self):
        """刷新任务列表"""
        # 清空现有卡片
        while self.task_layout.count():
            item = self.task_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.cards.clear()

        # 根据当前页面获取任务
        if self.current_page == "completed":
            tasks = self.manager.get_completed_tasks()
        else:
            tasks = self.manager.get_tasks()

        # 逆序添加任务卡片
        for task in reversed(tasks):
            self.create_card(task)

        self.task_layout.addStretch()

    def clear_tasks(self):
        """清空所有任务"""
        result = QMessageBox.warning(
            self,
            "确认",
            "确定清空所有任务吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:
            self.manager.clear_tasks()
            self.refresh()

    def change_page(self, page):
        """切换页面"""
        self.current_page = page
        self.refresh()

    def create_card(self, task):
        """创建任务卡片"""
        card = TaskCard(task)
        self.cards.append(card)
        self.tasks.append(task)
        self.task_layout.addWidget(card)

        card.delete_requested.connect(self.remove_task)
        card.status_changed.connect(self.update_task)
        card.edit_requested.connect(self.update_task)

    def add_task(self):
        """添加新任务"""
        text = self.input.text().strip()
        if not text:
            return

        self.manager.add_task(text)
        self.input.clear()
        self.refresh()

    def remove_task(self, card):
        """删除任务"""
        self.manager.delete_task(card.task.id)
        self.refresh()

    def update_task(self, task):
        """更新任务"""
        self.manager.update_task(task)
        self.refresh()

    def search(self, keyword):
        """搜索任务（根据关键词过滤卡片）"""
        keyword = keyword.lower()

        for card in self.cards:
            task = card.task
            content = (task.title + str(task.category) + str(task.priority)).lower()

            if keyword in content:
                card.show()
                card.highlight(keyword)
            else:
                card.hide()
