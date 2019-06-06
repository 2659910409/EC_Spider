from handle.website.base import Base
from handle.err_message import ErrorEnum
from handle.common.logging import logging
from handle.common.time import time


class SubReport(Base):
    def _operator_time_control(self, time):
        pass

    def operation_page(self):
        return True

    def operation_data_process(self):
        return True

    def operation_data_input(self):
        return True

    def operation_data_backup(self):
        return True


class SubReportDay(SubReport):
    def operation_page(self):
        param_time = None
        time.sleep(1.1)
        if not self._operator_time_control(param_time):
            logging.error('XXX 异常')
            self.error = ErrorEnum.ERROR_1001
            return False
        return True


class SubReportMonth(SubReport):
    def operation_page(self):
        return True
