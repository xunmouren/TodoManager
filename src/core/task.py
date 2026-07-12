from dataclasses import dataclass
from datetime import datetime

# 表示一个任务
@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    priority: str = "medium"
    category: str = "默认"
    created_time: str = ""
    deadline: str = ""

    def __post_init__(self):
        if not self.created_time:
            self.created_time = (datetime.now().strftime("%Y-%m-%d"))

    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "completed":self.completed,
            "priority":self.priority,
            "category": self.category,
            "created_time": self.created_time,
            "deadline": self.deadline
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data.get(
                "completed",
                False
            ),
            priority=data.get(
                "priority",
                "medium"
            ),
            category=data.get(
                "category",
                "默认"
            ),
            created_time=data.get(
                "created_time",
                ""
            ),
            deadline=data.get(
                "deadline",
                ""
            )
        )
