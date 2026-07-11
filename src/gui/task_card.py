from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QCheckBox
)


class TaskCard(QFrame):

    def __init__(self, title):

        super().__init__()

        self.title = title

        self.setup_ui()


    def setup_ui(self):

        layout = QHBoxLayout()


        self.checkbox = QCheckBox()
        self.setObjectName(
            "TaskCard"
        )


        self.label = QLabel(
            self.title
        )


        layout.addWidget(
            self.checkbox
        )

        layout.addWidget(
            self.label
        )


        self.setLayout(
            layout
        )


        self.setObjectName(
            "TaskCard"
        )