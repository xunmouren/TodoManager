from dataclasses import dataclass

# 表示一个任务
@dataclass
class Task:
    id: int
    title: str
    completed: bool = False