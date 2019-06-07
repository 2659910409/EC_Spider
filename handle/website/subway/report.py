from handle.website.base import Base
from handle.err_message import ErrorEnum
from handle.common.logging import logging
from handle.common.time import time
from retry import retry


class SubReport(Base):
    def _operator_time_control(self, start_time, end_time):

        pass

    @retry(tries=3, delay=2)
    def operation_page(self, url):
        try:
            self.web_driver.get(url) # 第一次请求到达平台默认页
            self.web_driver.close()
            self.web_driver.get(url)  # 第二次请求是为了到达指定的爬虫页

        except as e:
            print(e, '请求失败,请检查传入的url是否有效:{}'.format(url))

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
