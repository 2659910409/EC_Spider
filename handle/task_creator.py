from handle.common.private_logging import Logging


class TaskCreator:
    def __init__(self):
        pass

    def task_init(self):
        """初始化任务列表"""
        Logging.info('task_init')

    def task_added(self):
        """补入任务列表"""
        Logging.info('task_added')

    def get_task(self):
        """获取任务"""
        Logging.info('get_task')

    def task_finish(self):
        """
        任务执行结束检测
        1.等待任务执行结束，任务队列中无任务且没有进行中的任务
        2.执行任务结束后的任务，监控报告发送
        :return:
        """
        Logging.info('task_finish')
