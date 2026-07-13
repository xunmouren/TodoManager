from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal


class SearchBar(QLineEdit):
    """搜索框组件，支持实时搜索任务"""

    text_changed = Signal(str)

    def __init__(self):
        """初始化搜索框"""
        super().__init__()
        self.setPlaceholderText("🔍 搜索任务...")
        self.textChanged.connect(self.search)

    def search(self, text):
        """搜索文本变化时的处理函数"""
        self.text_changed.emit(text)
