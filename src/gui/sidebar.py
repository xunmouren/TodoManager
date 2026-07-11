from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)



class Sidebar(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()



    def setup_ui(self):
        self.setObjectName(
            "Sidebar"
        )

        self.setFixedWidth(
            220
        )


        layout = QVBoxLayout()


        title = QLabel(
            "TodoManager"
        )

        title.setObjectName(
            "SidebarTitle"
        )


        layout.addWidget(
            title
        )


        self.all_button = QPushButton(
            "📋 全部任务"
        )


        self.today_button = QPushButton(
            "📅 今日任务"
        )


        self.completed_button = QPushButton(
            "✅ 已完成"
        )


        layout.addWidget(
            self.all_button
        )

        layout.addWidget(
            self.today_button
        )

        layout.addWidget(
            self.completed_button
        )


        layout.addStretch()


        self.setLayout(
            layout
        )