from .task import Task
from .storage import Storage

class TaskManager:
    def __init__(self):
        self.storage = Storage()

    def get_tasks(self):
        data = self.storage.load()
        return [
            Task(
                id=item["id"],
                title=item["title"],
                completed=item["completed"]
            )
            for item in data
        ]

    def get_completed_tasks(self):
        return [task for task in self.get_tasks() if task.completed]

    def get_uncompleted_tasks(self):
        return [task for task in self.get_tasks() if not task.completed]

    def add_task(self, title):
        tasks = self.storage.load()
        new_id = max([item["id"] for item in tasks],default=0) + 1
        task = {
            "id": new_id,
            "title": title,
            "completed": False
        }
        tasks.append(task)
        self.storage.save(tasks)
        return Task(**task)

    def delete_task(self, task_id):
        tasks = self.storage.load()
        tasks = [
            item
            for item in tasks
            if item["id"] != task_id
        ]
        self.storage.save(tasks)
        self.reorder_ids()

    def update_task(self, task):
        tasks = self.storage.load()
        for item in tasks:
            if item["id"] == task.id:
                item["completed"] = task.completed
        self.storage.save(tasks)

    def reorder_ids(self):
        tasks = self.storage.load()
        for index, task in enumerate(tasks, start=1):
            task["id"] = index
        self.storage.save(tasks)
