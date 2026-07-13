from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel
)
from PySide6.QtGui import (
    QIcon,
    QDesktopServices
)
from PySide6.QtCore import (
    Qt,
    QSize,
    QUrl
)


class Footer(QWidget):
    """底部信息栏，包含社交链接和版权信息"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """构建底部栏界面"""
        self.setObjectName("Footer")
        self.setFixedHeight(36)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)

        # GitHub 按钮
        github = self.create_icon_button(
            "./icons/github.svg",
            "访问 GitHub",
            "https://github.com/xunmouren/TodoManager"
        )
        github.setObjectName("GitHubButton")

        # Bilibili 按钮
        bilibili = self.create_icon_button(
            "./icons/bilibili.svg",
            "访问 Bilibili",
            "https://space.bilibili.com/2052459252"
        )
        bilibili.setObjectName("BilibiliButton")

        # 版权信息
        copyright = QLabel("© 2026 TodoManager")
        copyright.setObjectName("CopyrightLabel")
        copyright.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(github)
        layout.addWidget(bilibili)
        layout.addStretch()
        layout.addWidget(copyright)

        self.setLayout(layout)

    def create_icon_button(self, icon, tooltip, url):
        """创建带图标和链接的按钮"""
        button = QPushButton()
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(24, 24))
        button.setFixedSize(33, 33)
        button.setFlat(True)
        button.setToolTip(tooltip)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(url))
        )
        return button