import json
from pathlib import Path

class Storage:
    """
    数据持久化存储类
    使用 JSON 格式保存任务数据到文件
    """
    def __init__(self):
        self.file = (Path(__file__).parent.parent.parent/ "data"/ "tasks.json")
        # 确保文件存在
        self.init_file()

    def init_file(self):
        """初始化数据文件"""
        # 如果文件不存在，创建一个空数组的 JSON 文件
        if not self.file.exists():
            self.file.write_text("[]",encoding="utf-8")

    def load(self):
        """从文件加载数据"""
        with open(self.file,"r",encoding="utf-8") as f:
            return json.load(f)

    def save(self,data):
        """保存数据到文件"""
        with open(self.file,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
