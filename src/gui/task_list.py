from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QComboBox,
    QMessageBox,
    QCheckBox,  # 添加
    QDialog,    # 添加
    QDialogButtonBox  # 添加
)
from PySide6.QtCore import Qt  # 添加 Signal

from ..core.manager import TaskManager
from ..core.category import get_category_items, get_category_keys
from .task_card import TaskCard
from .search_button import SearchButton


# 批量操作对话框
class BatchActionDialog(QDialog):
    """批量操作对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量操作")
        self.setFixedSize(300, 180)
        self.setObjectName("TaskEditor")
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        label = QLabel("请选择要执行的操作：")
        label.setStyleSheet("font-weight: 500; font-size: 14px;")
        
        self.action_combo = QComboBox()
        self.action_combo.addItem("✅ 标记为完成", "complete")
        self.action_combo.addItem("↩️ 标记为未完成", "uncomplete")
        self.action_combo.addItem("🗑 删除所选", "delete")
        self.action_combo.addItem("📁 修改分类", "category")
        
        self.category_combo = QComboBox()
        self.category_combo.setVisible(False)
        for key, name in get_category_items():
            self.category_combo.addItem(name, key)
        
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(label)
        layout.addWidget(self.action_combo)
        layout.addWidget(self.category_combo)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def on_action_changed(self, index):
        """切换操作时显示/隐藏分类选择框"""
        action = self.action_combo.currentData()
        self.category_combo.setVisible(action == "category")
    
    def get_action(self):
        """获取选中的操作"""
        return self.action_combo.currentData()
    
    def get_category(self):
        """获取选中的分类"""
        return self.category_combo.currentData()


class TaskList(QWidget):
    """任务列表主界面，支持分类、优先级管理和搜索"""

    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.current_page = "all"
        self.cards = []
        self.current_keyword = ""
        self.sort_by = "created"
        self.sort_reverse = True
        # 批量操作相关
        self.selected_cards = set()  # 选中的卡片集合
        self.batch_mode = False  # 是否处于批量模式
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """构建界面布局"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # 标题行（标题 + 批量操作按钮）
        header_layout = QHBoxLayout()
        title = QLabel("我的任务")
        title.setObjectName("PageTitle")
        
        # 批量操作按钮
        self.batch_toggle = QPushButton("☑ 批量操作")
        self.batch_toggle.setObjectName("BatchToggleButton")
        self.batch_toggle.setFixedHeight(32)
        self.batch_toggle.clicked.connect(self.toggle_batch_mode)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.batch_toggle)
        layout.addLayout(header_layout)

        # 批量操作工具栏（默认隐藏）
        self.batch_toolbar = QWidget()
        self.batch_toolbar.setVisible(False)
        self.batch_toolbar.setObjectName("BatchToolbar")
        self.batch_toolbar.setStyleSheet("""
            #BatchToolbar {
                background: #eef2ff;
                border-radius: 10px;
                padding: 8px 12px;
            }
        """)
        
        batch_layout = QHBoxLayout()
        batch_layout.setContentsMargins(0, 0, 0, 0)
        batch_layout.setSpacing(10)
        
        # 全选复选框
        self.select_all_checkbox = QCheckBox("全选")
        self.select_all_checkbox.stateChanged.connect(self.select_all_toggle)
        
        # 批量操作按钮
        self.batch_complete_btn = QPushButton("✅ 完成")
        self.batch_complete_btn.setObjectName("BatchCompleteBtn")
        self.batch_complete_btn.clicked.connect(lambda: self.batch_action("complete"))
        
        self.batch_uncomplete_btn = QPushButton("↩️ 未完成")
        self.batch_uncomplete_btn.setObjectName("BatchUncompleteBtn")
        self.batch_uncomplete_btn.clicked.connect(lambda: self.batch_action("uncomplete"))
        
        self.batch_delete_btn = QPushButton("🗑 删除")
        self.batch_delete_btn.setObjectName("BatchDeleteBtn")
        self.batch_delete_btn.clicked.connect(lambda: self.batch_action("delete"))
        
        self.batch_category_btn = QPushButton("📁 修改分类")
        self.batch_category_btn.setObjectName("BatchCategoryBtn")
        self.batch_category_btn.clicked.connect(self.batch_change_category)
        
        # 选中数量显示
        self.selected_count_label = QLabel("已选: 0 项")
        self.selected_count_label.setStyleSheet("color: #4f46e5; font-weight: 500;")
        
        batch_layout.addWidget(self.select_all_checkbox)
        batch_layout.addWidget(self.batch_complete_btn)
        batch_layout.addWidget(self.batch_uncomplete_btn)
        batch_layout.addWidget(self.batch_delete_btn)
        batch_layout.addWidget(self.batch_category_btn)
        batch_layout.addStretch()
        batch_layout.addWidget(self.selected_count_label)
        
        self.batch_toolbar.setLayout(batch_layout)
        layout.addWidget(self.batch_toolbar)

        # 搜索
        self.search_button = SearchButton()
        layout.addWidget(self.search_button)

        # 输入区域
        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("输入任务...")

        self.category_box = QComboBox()
        for key, name in get_category_items():
            self.category_box.addItem(name, key)

        self.priority_box = QComboBox()
        self.priority_box.addItem("🔴 高", "high")
        self.priority_box.addItem("🟡 中", "medium")
        self.priority_box.addItem("🟢 低", "low")
        self.priority_box.setCurrentIndex(1)

        self.add_button = QPushButton("+")
        self.add_button.setObjectName("AddButton")

        self.clear_button = QPushButton("🗑 清空")
        self.clear_button.setObjectName("ClearButton")

        input_row.addWidget(self.input)
        input_row.addWidget(self.category_box)
        input_row.addWidget(self.priority_box)
        input_row.addWidget(self.add_button)
        input_row.addWidget(self.clear_button)
        layout.addLayout(input_row)

        # 排序工具栏
        sort_layout = QHBoxLayout()
        sort_label = QLabel("排序：")
        sort_label.setStyleSheet("color: #6b7280; font-size: 13px;")
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("📅 创建时间", "created")
        self.sort_combo.addItem("📌 优先级", "priority")
        self.sort_combo.addItem("📆 截止日期", "deadline")
        self.sort_combo.addItem("🔤 标题", "title")
        self.sort_combo.setCurrentIndex(0)
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        
        self.sort_order_button = QPushButton("↓")
        self.sort_order_button.setFixedSize(30, 30)
        self.sort_order_button.setToolTip("切换排序方向")
        self.sort_order_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #eef2ff;
                border-color: #818cf8;
            }
        """)
        self.sort_order_button.clicked.connect(self.toggle_sort_order)
        
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addWidget(self.sort_order_button)
        sort_layout.addStretch()
        layout.addLayout(sort_layout)

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

    # ===== 批量操作方法 =====
    
    def toggle_batch_mode(self):
        """切换批量模式"""
        self.batch_mode = not self.batch_mode
        self.batch_toolbar.setVisible(self.batch_mode)
        self.batch_toggle.setText("☑ 退出批量" if self.batch_mode else "☑ 批量操作")
        
        # 清除所有选中
        self.selected_cards.clear()
        self.select_all_checkbox.setChecked(False)
        self.update_selected_count()
        
        # 显示/隐藏卡片复选框
        for card in self.cards:
            card.set_batch_mode(self.batch_mode)
            if not self.batch_mode:
                card.set_checked(False)
    
    def select_all_toggle(self, state):
        """全选/取消全选"""
        if state == Qt.Checked:
            for card in self.cards:
                if card.isVisible():
                    card.set_checked(True)
                    self.selected_cards.add(card)
        else:
            for card in self.cards:
                card.set_checked(False)
                self.selected_cards.discard(card)
        self.update_selected_count()
    
    def on_card_selected(self, card, selected):
        """卡片选中状态变化"""
        if selected:
            self.selected_cards.add(card)
        else:
            self.selected_cards.discard(card)
        self.update_selected_count()
        
        # 更新全选状态
        visible_cards = [c for c in self.cards if c.isVisible()]
        if visible_cards and all(c.is_checked() for c in visible_cards):
            self.select_all_checkbox.setChecked(True)
        else:
            self.select_all_checkbox.setChecked(False)
    
    def update_selected_count(self):
        """更新选中数量显示"""
        count = len(self.selected_cards)
        self.selected_count_label.setText(f"已选: {count} 项")
        
        # 启用/禁用批量操作按钮
        has_selected = count > 0
        self.batch_complete_btn.setEnabled(has_selected)
        self.batch_uncomplete_btn.setEnabled(has_selected)
        self.batch_delete_btn.setEnabled(has_selected)
        self.batch_category_btn.setEnabled(has_selected)
    
    def batch_action(self, action):
        """执行批量操作"""
        if not self.selected_cards:
            return
        
        # 确认操作
        action_names = {
            "complete": "标记为完成",
            "uncomplete": "标记为未完成",
            "delete": "删除"
        }
        
        if action == "delete":
            msg = QMessageBox(self)
            msg.setWindowTitle("确认删除")
            msg.setText(f"确定要删除选中的 {len(self.selected_cards)} 个任务吗？")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.button(QMessageBox.Yes).setText("是")
            msg.button(QMessageBox.No).setText("否")
            if msg.exec() != QMessageBox.Yes:
                return
        
        # 执行操作
        for card in list(self.selected_cards):
            task = card.task
            if action == "complete":
                task.completed = True
                card.checkbox.setChecked(True)
                self.manager.update_task(task)
            elif action == "uncomplete":
                task.completed = False
                card.checkbox.setChecked(False)
                self.manager.update_task(task)
            elif action == "delete":
                self.manager.delete_task(task.id)
        
        # 退出批量模式并刷新
        self.toggle_batch_mode()
        self.refresh()
        
        # 显示成功消息
        if action != "delete":
            msg = QMessageBox(self)
            msg.setWindowTitle("完成")
            msg.setText(f"已成功{action_names.get(action, '操作')} {len(self.selected_cards)} 个任务")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
    
    def batch_change_category(self):
        """批量修改分类"""
        if not self.selected_cards:
            return
        
        # 弹出分类选择对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("修改分类")
        dialog.setFixedSize(300, 120)
        dialog.setObjectName("TaskEditor")
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        label = QLabel("选择新的分类：")
        category_combo = QComboBox()
        for key, name in get_category_items():
            category_combo.addItem(name, key)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addWidget(label)
        layout.addWidget(category_combo)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            new_category = category_combo.currentData()
            for card in list(self.selected_cards):
                card.task.category = new_category
                self.manager.update_task(card.task)
                card.update_info()
            
            # 退出批量模式
            self.toggle_batch_mode()
            self.refresh()
            
            msg = QMessageBox(self)
            msg.setWindowTitle("完成")
            msg.setText(f"已成功修改 {len(self.selected_cards)} 个任务的分类")
            msg.setIcon(QMessageBox.Information)
            msg.exec()

    # ===== 排序方法 =====
    
    def on_sort_changed(self):
        self.sort_by = self.sort_combo.currentData()
        self.refresh()

    def toggle_sort_order(self):
        self.sort_reverse = not self.sort_reverse
        self.sort_order_button.setText("↓" if self.sort_reverse else "↑")
        self.sort_order_button.setToolTip("切换排序方向（当前：{}）".format("降序" if self.sort_reverse else "升序"))
        self.refresh()

    def sort_tasks(self, tasks):
        if self.sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            tasks.sort(key=lambda t: priority_order.get(t.priority, 1), reverse=self.sort_reverse)
        elif self.sort_by == "deadline":
            def deadline_key(t):
                return t.deadline if t.deadline else "9999-99-99"
            tasks.sort(key=deadline_key, reverse=self.sort_reverse)
        elif self.sort_by == "title":
            tasks.sort(key=lambda t: t.title.lower(), reverse=self.sort_reverse)
        else:
            tasks.sort(key=lambda t: t.id, reverse=self.sort_reverse)
        return tasks

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
        elif self.current_page in get_category_keys():
            tasks = self.manager.get_tasks_by_category(self.current_page)
        else:
            tasks = self.manager.get_tasks()

        tasks = self.sort_tasks(tasks)

        for task in tasks:
            card = TaskCard(task)
            self.task_layout.addWidget(card)
            self.cards.append(card)
            
            card.delete_requested.connect(self.remove_task)
            card.status_changed.connect(self.update_task)
            card.edit_requested.connect(self.update_task)
            # 连接批量选择信号
            card.selection_changed.connect(self.on_card_selected)

        self.task_layout.addStretch()

        if self.current_keyword:
            self.apply_highlight(self.current_keyword)
        
        # 如果处于批量模式，重新设置卡片状态
        if self.batch_mode:
            for card in self.cards:
                card.set_batch_mode(True)
                if card in self.selected_cards:
                    card.set_checked(True)
            self.update_selected_count()

    def remove_task(self, card):
        self.manager.delete_task(card.task.id)
        self.refresh()

    def update_task(self, task):
        self.manager.update_task(task)
        self.refresh()

    def add_task(self):
        text = self.input.text().strip()
        if not text:
            return

        category = self.category_box.currentData()
        priority = self.priority_box.currentData()
        self.manager.add_task(text, category, priority)
        self.input.clear()
        self.refresh()

    def change_page(self, page):
        self.current_page = page
        self.current_keyword = ""
        # 切换页面时退出批量模式
        if self.batch_mode:
            self.toggle_batch_mode()
        self.refresh()

    def search(self, keyword):
        self.current_keyword = keyword.strip()
        self.apply_highlight(self.current_keyword)

    def apply_highlight(self, keyword):
        keyword_lower = keyword.lower()
        
        for card in self.cards:
            if keyword_lower:
                title_lower = card.task.title.lower()
                if keyword_lower in title_lower:
                    card.show()
                    card.highlight(keyword)
                else:
                    card.hide()
                    card.highlight("")
            else:
                card.show()
                card.highlight("")

    def clear_tasks(self):
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
