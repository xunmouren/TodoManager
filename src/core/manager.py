from .task import Task
from .storage import Storage

class TaskManager:
    """
    任务数据管理器
    负责所有数据操作：增、删、改、查
    是界面层和数据存储层之间的桥梁
    """
    def __init__(self):
        self.storage = Storage()

    def get_tasks(self):
        """获取所有任务"""
        # 从存储加载原始数据(字典列表)
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
        """获取已完成的任务列表"""
        return [task for task in self.get_tasks() if task.completed]

    def get_uncompleted_tasks(self):
        """获取未完成的任务列表"""
        return [task for task in self.get_tasks() if not task.completed]

    def add_task(self, title):
        """添加新任务"""
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
        """删除指定ID的任务"""
        tasks = self.storage.load()
        # 使用列表推导式过滤掉要删除的任务
        tasks = [
            item
            for item in tasks
            if item["id"] != task_id
        ]
        self.storage.save(tasks)
        self.reorder_ids()

    def update_task(self, task):
        """更新任务"""
        tasks = self.storage.load()
        for item in tasks:
            if item["id"] == task.id:
                item["title"] = task.title
                item["completed"] = task.completed
        self.storage.save(tasks)

    def reorder_ids(self):
        """重新编号"""
        tasks = self.storage.load()
        for index, task in enumerate(tasks, start=1):
            task["id"] = index
        self.storage.save(tasks)
