from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QComboBox,
    QMessageBox
)
from PySide6.QtCore import Qt

from ..core.manager import TaskManager
from ..core.category import get_category_items, get_category_keys
from .task_card import TaskCard
from .search_button import SearchButton


class TaskList(QWidget):
    """任务列表主界面，支持分类、优先级管理和搜索"""

    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.current_page = "all"
        self.cards = []
        self.current_keyword = ""  #  保存当前搜索关键词
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """构建界面布局"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # 标题
        title = QLabel("我的任务")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        # 搜索
        self.search_button = SearchButton()
        layout.addWidget(self.search_button)

        # 输入区域
        self.input = QLineEdit()
        self.input.setPlaceholderText("输入任务...")

        # 分类选择
        self.category_box = QComboBox()
        for key, name in get_category_items():
            self.category_box.addItem(name, key)

        # 优先级选择
        self.priority_box = QComboBox()
        self.priority_box.addItem("🔴 高", "high")
        self.priority_box.addItem("🟡 中", "medium")
        self.priority_box.addItem("🟢 低", "low")
        self.priority_box.setCurrentIndex(1)

        # 按钮
        self.add_button = QPushButton("+")
        self.add_button.setObjectName("AddButton")

        self.clear_button = QPushButton("🗑 清空")
        self.clear_button.setObjectName("ClearButton")

        # 输入布局
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.category_box)
        input_layout.addWidget(self.priority_box)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.clear_button)
        layout.addLayout(input_layout)

        # 任务列表
        self.container = QWidget()
        self.container.setObjectName("TaskContainer")
        
        self.task_layout = QVBoxLayout()
        self.task_layout.setAlignment(Qt.AlignTop)
        self.task_layout.setSpacing(10)
        self.task_layout.setContentsMargins(15, 15, 15, 15)
        self.container.setLayout(self.task_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)
        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)
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
        elif self.current_page in get_category_keys():
            tasks = self.manager.get_tasks_by_category(self.current_page)
        else:
            tasks = self.manager.get_tasks()

        # 创建任务卡片
        for task in tasks:
            card = TaskCard(task)
            self.task_layout.addWidget(card)
            self.cards.append(card)
            
            card.delete_requested.connect(self.remove_task)
            card.status_changed.connect(self.update_task)
            card.edit_requested.connect(self.update_task)

        self.task_layout.addStretch()

        #  刷新后如果有搜索关键词，重新应用高亮
        if self.current_keyword:
            self.apply_highlight(self.current_keyword)

    def remove_task(self, card):
        """删除任务"""
        self.manager.delete_task(card.task.id)
        self.refresh()

    def update_task(self, task):
        """更新任务"""
        self.manager.update_task(task)
        self.refresh()

    def add_task(self):
        """添加新任务"""
        text = self.input.text().strip()
        if not text:
            return

        category = self.category_box.currentData()
        priority = self.priority_box.currentData()
        self.manager.add_task(text, category, priority)
        self.input.clear()
        self.refresh()

    def change_page(self, page):
        """切换页面"""
        self.current_page = page
        self.current_keyword = ""  #  切换页面时清空搜索关键词
        self.refresh()

    #  修改 search 方法
    def search(self, keyword):
        """搜索任务（根据标题关键词过滤并高亮）"""
        self.current_keyword = keyword.strip()
        self.apply_highlight(self.current_keyword)

    #  新增高亮方法
    def apply_highlight(self, keyword):
        """应用高亮到所有卡片"""
        keyword_lower = keyword.lower()
        
        for card in self.cards:
            if keyword_lower:
                # 有关键词：检查是否匹配
                title_lower = card.task.title.lower()
                if keyword_lower in title_lower:
                    card.show()
                    card.highlight(keyword)  # 调用卡片的高亮方法
                else:
                    card.hide()
                    card.highlight("")  # 清除高亮
            else:
                # 无关键词：显示所有卡片，清除高亮
                card.show()
                card.highlight("")

    def clear_tasks(self):
        """清空所有任务"""
        msg = QMessageBox(self)
        msg.setWindowTitle("确认")
        msg.setText("确定删除所有任务吗？")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("是")
        msg.button(QMessageBox.No).setText("否")

        if msg.exec() == QMessageBox.Yes:
            self.manager.clear_tasks()
            self.refresh()
