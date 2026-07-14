from .task import Task
from .storage import Storage


class TaskManager:
    """任务数据管理器，负责任务增删改查"""

    def __init__(self):
        self.storage = Storage()

    def get_tasks(self):
        """获取所有任务"""
        data = self.storage.load()
        tasks = []
        for item in data:
            # 兼容旧数据
            if "category" not in item:
                item["category"] = "default"
            tasks.append(Task.from_dict(item))
        return tasks

    def get_tasks_by_category(self, category):
        """根据分类获取任务"""
        tasks = self.get_tasks()
        if category == "all":
            return tasks
        return [task for task in tasks if task.category == category]

    def get_completed_tasks(self):
        """获取已完成任务"""
        return [task for task in self.get_tasks() if task.completed]

    def get_uncompleted_tasks(self):
        """获取未完成任务"""
        return [task for task in self.get_tasks() if not task.completed]

    def add_task(self, title, category="默认"):
        """添加任务"""
        tasks = self.get_tasks()
        new_id = max([task.id for task in tasks], default=0) + 1
        task = Task(id=new_id, title=title, category=category)
        tasks.append(task)
        self.save_tasks(tasks)
        return task

    def delete_task(self, task_id):
        """删除任务"""
        tasks = self.storage.load()
        tasks = [item for item in tasks if item["id"] != task_id]
        self.storage.save(tasks)
        self.reorder_ids()

    def update_task(self, task):
        """更新任务"""
        tasks = self.get_tasks()
        for index, item in enumerate(tasks):
            if item.id == task.id:
                tasks[index] = task
        self.save_tasks(tasks)

    def reorder_ids(self):
        """重新编号"""
        tasks = self.storage.load()
        for index, task in enumerate(tasks, start=1):
            task["id"] = index
        self.storage.save(tasks)

    def save_tasks(self, tasks):
        """保存任务列表"""
        self.storage.save([task.to_dict() for task in tasks])

    def clear_tasks(self):
        """清空所有任务"""
        self.storage.save([])
