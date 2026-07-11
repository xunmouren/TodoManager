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

        self.cards = []

        self.setup_ui()


    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setSpacing(15)


        # 页面标题
        title = QLabel(
            "我的任务"
        )

        title.setObjectName(
            "PageTitle"
        )


        # 输入框
        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "输入任务..."
        )


        # 添加按钮
        self.add_button = QPushButton(
            "＋ 添加任务"
        )

        self.add_button.setObjectName(
            "AddButton"
        )


        # 任务区域
        self.task_layout = QVBoxLayout()

        self.task_layout.setSpacing(
            10
        )


        # 添加组件

        layout.addWidget(
            title
        )


        layout.addWidget(
            self.input
        )


        layout.addWidget(
            self.add_button
        )


        layout.addSpacing(
            10
        )


        layout.addLayout(
            self.task_layout
        )


        layout.addStretch()


        self.setLayout(
            layout
        )


        # 信号

        self.add_button.clicked.connect(
            self.add_task
        )

        self.input.returnPressed.connect(
            self.add_task
        )


    def add_task(self):

        text = self.input.text().strip()


        if not text:

            return


        card = TaskCard(
            text
        )


        self.cards.append(
            card
        )


        self.task_layout.addWidget(
            card
        )


        card.delete_requested.connect(
            self.remove_task
        )


        self.input.clear()



    def remove_task(self, card):

        if card in self.cards:

            self.cards.remove(
                card
            )


        self.task_layout.removeWidget(
            card
        )


        card.deleteLater()