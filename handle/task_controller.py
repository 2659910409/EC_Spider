from handle.err_message import ErrorEnum
from common.private_logging import Logging
from handle.task_creator import TaskCreator
from handle.login import tb_login
from handle.website.subway.spread_report import SpreadReportDay


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
        self.obj_name = name
        self.obj_param = param
        self.obj = None
        self.error = None
        try:
            Logging.info(self.obj_name, self.obj_param, ' 实例化 start!')
            if self.obj_name == 'handle.task_creator.TaskCreator':
                self.obj = TaskCreator()
            elif self.obj_name == 'handle.login.tb_login.TaoLogin':
                self.obj = tb_login()
            # ========================== 抓取页面实例配置 ==========================
            elif self.obj_name == 'handle.website.subway.report.SubReportDay':
                self.obj = SpreadReportDay(self.obj_param['store_id'], self.obj_param['page_data_id'], self.obj_param['port'])
            # ========================== 抓取页面实例配置 ==========================
            else:
                self.error = ErrorEnum.ERROR_9001
                self.error.value.set_msg(('未匹配到任务实例 name:' + self.obj_name + ',param:' + self.obj_param))
            Logging.info(self.obj_name, self.obj_param, ' 实例化 end!')
        except Exception as e:
            Logging.error(e)
            if self.is_success() and self.obj and self.obj.error:
                self.error = self.obj.error
            self.error = ErrorEnum.ERROR_9999

    def get_obj(self):
        return self.obj

    def is_success(self):
        if self.error is None:
            return True
        return False

    def run(self, func, param={}):
        """
        对象任务执行调度控制模板
        :param func:
        :return:
        """
        try:
            Logging.info(self.obj_name, func, param, ' 步骤执行 start!')
            if self.obj_name == 'handle.task_creator.TaskCreator' and func == 'task_init':
                results = self.obj.task_init()
            elif self.obj_name == 'handle.task_creator.TaskCreator' and func == 'task_added':
                results = self.obj.task_added()
            elif self.obj_name == 'handle.task_creator.TaskCreator' and func == 'get_task':
                results = self.obj.get_task()
            elif self.obj_name == 'handle.task_creator.TaskCreator' and func == 'task_finish':
                results = self.obj.task_finish()
            elif self.obj_name == 'handle.task_creator.TaskCreator' and func == 'task_set_start':
                results = self.obj.task_set_start(param)
            elif self.obj_name == 'handle.task_creator.TaskCreator' and func == 'task_set_end':
                results = self.obj.task_set_end(param)
            elif self.obj_name == 'handle.login.tb_login.TaoLogin' and func == 'run':
                results = self.obj.task_set_end(param)
            elif self.obj_name.find('handle.website') == 0 and func == 'operation_page':
                results = self.obj.operation_page()
            elif self.obj_name.find('handle.website') == 0 and func == 'operation_page_download':
                results = self.obj.operation_page_download()
            elif self.obj_name.find('handle.website') == 0 and func == 'operation_data_process':
                results = self.obj.operation_page()
            elif self.obj_name.find('handle.website') == 0 and func == 'operation_data_input':
                results = self.obj.operation_page()
            elif self.obj_name.find('handle.website') == 0 and func == 'operation_data_backup':
                results = self.obj.operation_page()
            else:
                self.error = ErrorEnum.ERROR_9002
                self.error.value.set_msg(('未匹配到任务func name:'+self.obj_name+',func:'+func))
            Logging.info(self.obj_name, func, param, ' 步骤执行 end!')
        except Exception as e:
            Logging.error(e)
            self.error = self.obj.error
            raise Exception
        return results
