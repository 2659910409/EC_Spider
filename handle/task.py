from common.db import DataBase


class Task:
    """
    任务对象基类
    """
    def __init__(self):
        self.error = None
        self.db = DataBase()

    def is_success(self):
        if self.error is None:
            return True
        return False

    def get_error(self):
        return self.error.value

    def set_error_msg(self, msg):
        self.error.value.set_msg(msg)
