import json
from pathlib import Path


class Config:
    """应用配置管理"""

    def __init__(self):
        self.file = Path(__file__).parent.parent.parent / "data" / "settings.json"
        self.init_file()

    def init_file(self):
        """创建默认配置文件"""
        if not self.file.exists():
            self.save({
                "theme": "light",
                "color": "#6366f1",
                "font_size": 14,
                "shortcuts": {
                    "search": "Ctrl+F",
                    "add": "Ctrl+N"
                }
            })

    def load(self):
        """加载配置"""
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        """保存配置"""
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
