from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea
)
from PySide6.QtCore import Qt
from core.manager import TaskManager
from .task_card import TaskCard


class TaskList(QWidget):
    """
    任务列表主界面
    负责显示、添加、删除和管理任务卡片
    """

    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.cards = []
        self.current_page = "all"
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """构建界面布局"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("我的任务")
        title.setObjectName("PageTitle")

        self.input = QLineEdit()
        self.input.setPlaceholderText("输入任务...")

        self.add_button = QPushButton("+ 添加任务")
        self.add_button.setObjectName("AddButton")

        # ===== 任务滚动区域 =====
        self.task_container = QWidget()
        self.task_container.setObjectName("TaskContainer")
        
        self.task_layout = QVBoxLayout()
        self.task_layout.setSpacing(10)
        self.task_layout.setContentsMargins(10, 10, 10, 10)
        self.task_layout.setAlignment(Qt.AlignTop)
        self.task_container.setLayout(self.task_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(360)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setWidget(self.task_container)

        layout.addWidget(title)
        layout.addWidget(self.input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.scroll_area)
        layout.addStretch()

        self.setLayout(layout)
        self.add_button.clicked.connect(self.add_task)
        self.input.returnPressed.connect(self.add_task)

    def refresh(self):
        """刷新任务列表"""
        while self.task_layout.count():
            item = self.task_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.cards.clear()

        if self.current_page == "completed":
            tasks = self.manager.get_completed_tasks()
        else:
            tasks = self.manager.get_tasks()

        for task in reversed(tasks):
            self.create_card(task)
        
        self.task_layout.addStretch()

    def change_page(self, page):
        """切换当前显示的页面"""
        self.current_page = page
        self.refresh()

    def create_card(self, task):
        """创建任务卡片并添加到列表中"""
        card = TaskCard(task)
        self.cards.append(card)
        self.task_layout.addWidget(card)
        card.delete_requested.connect(self.remove_task)
        card.status_changed.connect(self.update_task)
        card.edit_requested.connect(self.update_task)

    def add_task(self):
        text = self.input.text().strip()
        if not text:
            return
        self.manager.add_task(text)
        self.input.clear()
        self.refresh()

    def remove_task(self, card):
        self.manager.delete_task(card.task.id)
        self.refresh()

    def update_task(self, task):
        self.manager.update_task(task)
        self.refresh()