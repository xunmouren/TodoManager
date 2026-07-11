from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit
)

from .task_card import TaskCard



class TaskList(QWidget):

    def __init__(self):

        super().__init__()

        self.tasks = []

        self.setup_ui()



    def setup_ui(self):

        layout = QVBoxLayout()


        title = QLabel(
            "我的任务"
        )

        title.setObjectName(
            "PageTitle"
        )


        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "输入任务..."
        )


        self.add_button = QPushButton(
            "添加任务"
        )


        self.task_layout = QVBoxLayout()


        layout.addWidget(title)

        layout.addWidget(
            self.input
        )

        layout.addWidget(
            self.add_button
        )


        layout.addLayout(
            self.task_layout
        )


        layout.addStretch()


        self.setLayout(
            layout
        )


        # 信号连接

        self.add_button.clicked.connect(
            self.add_task
        )



    def add_task(self):

        text = self.input.text()


        if not text:
            return


        card = TaskCard(text)


        self.task_layout.addWidget(
            card
        )


        self.input.clear()