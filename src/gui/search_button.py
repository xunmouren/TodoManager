from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit
)
from PySide6.QtCore import (
    Signal,
    QPropertyAnimation,
    QEasingCurve,
    Qt  # 添加 Qt 模块
)
from PySide6.QtGui import QIcon


class SearchButton(QWidget):
    """可展开的搜索按钮，点击后平滑展开搜索输入框"""

    search_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.expanded = False
        self.animation = None
        self.setup_ui()

    def setup_ui(self):
        """构建UI组件"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # 无间距，按钮和输入框紧挨着

        # 添加弹性空间，把按钮推到最右边
        layout.addStretch()

        # 搜索按钮
        self.button = QPushButton()
        self.button.setIcon(QIcon("icons/search.svg"))
        self.button.setFixedSize(40, 40)
        self.button.setCursor(Qt.PointingHandCursor)  # 鼠标悬停变为手型

        # 搜索输入框（初始宽度为0，隐藏状态）
        self.input = QLineEdit()
        self.input.setObjectName("SearchInput")
        self.input.setPlaceholderText("搜索任务...")
        self.input.setMaximumWidth(0)
        self.input.setAlignment(Qt.AlignLeft)  # 文字左对齐

        # 先添加输入框，再添加按钮（按钮在最右边）
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # 连接信号
        self.button.clicked.connect(self.toggle)
        self.input.textChanged.connect(self.search_changed.emit)

    def toggle(self):
        """切换搜索框展开/收起状态"""
        self.expanded = not self.expanded

        # 创建宽度动画
        self.animation = QPropertyAnimation(self.input, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        if self.expanded:
            # 展开：宽度从0到220，从右向左弹出
            self.animation.setStartValue(0)
            self.animation.setEndValue(400)
            self.input.setFocus()
            self.input.selectAll()
        else:
            # 收起：宽度从220到0
            self.animation.setStartValue(400)
            self.animation.setEndValue(0)
            self.input.clear()

        self.animation.start()

        # =====以下是原来的弹出动画代码=====
        # if self.expanded:
        #     # 展开：宽度从0到220
        #     self.animation.setStartValue(0)
        #     self.animation.setEndValue(220)
        #     self.input.setFocus()
        # else:
        #     # 收起：宽度从220到0
        #     self.animation.setStartValue(220)
        #     self.animation.setEndValue(0)
        #     self.input.clear()

    def open_search(self):
        """外部调用的展开搜索方法"""
        if not self.expanded:
            self.toggle()
        self.input.setFocus()
