#!/usr/bin/env python
# -*- coding: UTF8 -*-


# TODO 填充框架
class WorkerService:
    """工人服务，注册service，可通过worker调度启动其他worker"""
    def __init__(self, name, heartbeats):
        self.name = name
        self.heartbeats = heartbeats
        self.status = '空闲'
        self.host = None
        self.pid = None
        pass

    def heartbeat(self):
        # status:空闲(心跳每3秒)
        queue = []
        if len(queue) > 0:
            self.get_work()
        pass

    def get_work(self):
        # get_work 从任务队列中获取工作
        pass

    def handle(self):
        # status:工作中
        pass
