from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea
)
from core.manager import TaskManager
from .task_card import TaskCard


class TaskList(QWidget):
    """
    任务列表主界面
    负责显示、添加、删除和管理任务卡片
    """

    def __init__(self):
        super().__init__()
        # 创建任务管理器实例
        self.manager = TaskManager()
        # 存储当前显示的任务卡片对象列表
        self.cards = []
        # 当前显示的页面类型："all" 或 "completed"
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

        # 任务滚动区域
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        # 卡片间距
        self.task_layout.setSpacing(12)
        self.task_layout.setContentsMargins(5,5,5,5)
        self.task_container.setLayout(self.task_layout)
        self.scroll_area = QScrollArea()
        # 让内容自适应
        self.scroll_area.setWidgetResizable(True)
        # 最小高度
        self.scroll_area.setMinimumHeight(500)
        # 无边框
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setWidget(self.task_container)

        layout.addWidget(title)
        layout.addWidget(self.input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.scroll_area,1)

        # 连接信号：点击按钮或按回车键都可以添加任务
        self.setLayout(layout)
        self.add_button.clicked.connect(self.add_task)
        self.input.returnPressed.connect(self.add_task)

    def refresh(self):
        """
        刷新任务列表
        清空当前显示的所有卡片，从数据库重新加载并显示
        """
        # 清空布局中的所有组件
        while self.task_layout.count():
            item = self.task_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 清空卡片列表
        self.cards.clear()

        # 根据当前页面类型获取对应的任务数据
        if self.current_page == "completed":
            tasks = self.manager.get_completed_tasks()
        else:
            tasks = self.manager.get_tasks()

        # 为每个任务创建并添加卡片
        for task in tasks:
            self.create_card(task)

    def change_page(self, page):
        """
        切换页面
        由侧边栏的 page_changed 信号触发
        """
        self.current_page = page
        self.refresh()

    def create_card(self, task):
        """创建一个任务卡片并添加到界面"""
        card = TaskCard(task)
        self.cards.append(card)
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
        """更新任务（状态或标题变更时调用）"""
        self.manager.update_task(task)
        self.refresh()
