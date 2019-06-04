#!/usr/bin/env python
# -*- coding: UTF8 -*-


# TODO 填充框架
# Flask/Redis：
# worker_${pid}：{status:工作中/空闲, queue:1, start_time:123, heartbeat:155550001} # worker状态信息
# worker_${pid}_queue：[{task_id:1, params:{}}] # worker任务队列：队列方式先进先出原则
class MasterService:
    """管理服务"""
    def __init__(self):
        pass

    def init_workers(self):
        pass

    def get_workers(self):
        pass

    def worker_creator(self):
        # 创建一个worker,pid
        pass

    def worker_kill(self):
        # 停止,pid
        pass

    def worker_status(self):
        # 获取worker信息,pid
        pass
