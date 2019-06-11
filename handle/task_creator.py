from handle.common.logging import Logging


class TaskCreator:
    def __init__(self):
        pass

    def task_init(self):
        """初始化任务列表"""
        Logging.info('task_init')

    def task_added(self):
        """补入任务列表"""
        Logging.info('task_added')
