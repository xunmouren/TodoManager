from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from core.manager import TaskManager
from .task_card import TaskCard


class TaskList(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.cards = []
        self.current_page = "all"
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("我的任务")
        title.setObjectName("PageTitle")

        self.input = QLineEdit()
        self.input.setPlaceholderText("输入任务...")

        self.add_button = QPushButton("＋ 添加任务")
        self.add_button.setObjectName("AddButton")

        self.task_layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.input)
        layout.addWidget(self.add_button)
        layout.addLayout(self.task_layout)
        layout.addStretch()

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_task)
        self.input.returnPressed.connect(self.add_task)

    def refresh(self):
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
        for task in tasks:
            self.create_card(task)

    def change_page(self, page):
        self.current_page = page
        self.refresh()

    def create_card(self, task):
        card = TaskCard(task)
        self.cards.append(card)
        self.task_layout.addWidget(card)
        card.delete_requested.connect(self.remove_task)
        card.status_changed.connect(self.update_task)

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
