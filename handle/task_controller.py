from handle.common.logging import Logging
from handle.task_creator import TaskCreator
from handle.err_message import ErrorEnum


class TaskController:
    """
    任务调度控制
    """
    def __init__(self, name, param={}):
        """
        对象/任务实例化
        :param name: 对象标识，规则：从目录至最终对象，handle.xxx.Obj
        :param param: 对象实例化参数，类型：dict
        """
        self.name = name
        self.param = param
        self.error = None
        try:
            if name == 'handle.task_creator.TaskCreator':
                Logging.info(name,)
                self.obj = TaskCreator()
            else:
                self.error = ErrorEnum.ERROR_9001
                self.error.value.set_msg(('未匹配到任务实例 name:'+name+',param:'+param))
        except Exception as e:
            Logging.error(e)
            self.error = self.obj.error

    def get_obj(self):
        return self.obj

    def is_success(self):
        if self.error is None:
            return True
        return False

    def run(self, func):
        """
        对象任务执行调度控制模板
        :param func:
        :return:
        """
        try:
            if self.name == 'handle.task_creator.TaskCreator' and func == 'task_init':
                results = self.obj.task_init()
            elif self.name == 'handle.task_creator.TaskCreator' and func == 'task_added':
                results = self.obj.task_added()
            else:
                self.error = ErrorEnum.ERROR_9002
                self.error.value.set_msg(('未匹配到任务func name:'+self.name+',func:'+func))
        except Exception as e:
            Logging.error(e)
            self.error = self.obj.error
            raise Exception
        return results
