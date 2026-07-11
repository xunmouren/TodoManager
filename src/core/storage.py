import json
from pathlib import Path

class Storage:
    def __init__(self):
        self.file = (Path(__file__).parent.parent.parent/ "data"/ "tasks.json")
        self.init_file()

    def init_file(self):
        if not self.file.exists():
            self.file.write_text("[]",encoding="utf-8")

    def load(self):
        with open(self.file,"r",encoding="utf-8") as f:
            return json.load(f)

    def save(self,data):
        with open(self.file,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
