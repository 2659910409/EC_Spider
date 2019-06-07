from handle.website.base import Base
from handle.err_message import ErrorEnum
from handle.common import logging
from handle.common import time
from retry import retry


class SpreadReport(Base):
    def _operator_time_control(self, start_date=None, end_date=None):
        """
        :param start_date: 日期区间的开始日期,需自定义日期报表时指定
        :param end_date: 日期区间的结束日期,需自定义日期报表时指定
        :return: True/False
        """
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').send_keys(time.date_to_string(start_date))
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').send_keys(time.date_to_string(end_date))
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').click()


    def _operator_period_control(self, num=15):
        """
        :param num:
        :return:
        """
        self.web_driver.find_element_in_xpath('').click()

    def _operator_point_control(self):
        """   """
        self.web_driver.find_element_in_xpath('').pop().click() # 取消已有勾选框
        self.web_driver.find_element_in_xpath('').pop().click()
        self.web_driver.find_element_in_xpath('').click() # 点击需要勾选的条件
        self.web_driver.find_element_in_xpath('').click()
        self.web_driver.find_element_in_xpath('').click() # 点击确定使条件生效
        # self.web_driver.find_element_in_xpath('').pop().click()
        # self.web_driver.find_element_in_xpath('').pop().click()
        # self.web_driver.find_element_in_xpath('').click()
        # self.web_driver.find_element_in_xpath('').click()

    def _locate_page(self,url):
        """
        :param url: 指定抓取页面的url
        :return: True/False
        """
        try:
            self.web_driver.get(url) # 第一次请求到达平台默认页
            self.web_driver.close()
            self.web_driver.get(url)  # 第二次请求是为了到达指定的爬虫页
        except as e:
            print(e, '请求失败,请检查传入的url是否有效:{}'.format(url))
            return False
        return True

    @retry(tries=3, delay=2)
    def operation_page(self, num=None, report_type=None, start_date=None, end_date=None):
        """
        :param num: 转化周期筛选
        :param report_type: 报表类型,目前支持日报'day',月报'month',及自定义日期区间的报表
        :param start_date: 日期区间的开始日期,需自定义日期报表时指定
        :param end_date: 日期区间的结束日期,需自定义日期报表时指定
        :return: True/False
        """
        return True

    def download_file(self):
        pass

    def operation_data_process(self):
        return True

    def operation_data_input(self):
        return True

    def operation_data_backup(self):
        return True
    pass


class SpreadReportDay(SubReport):
    @retry(tries=3, delay=2)
    def operation_page(self, url, num=None):
        """
        :param url: 指定抓取页面的url
        :param num: 转化周期筛选
        :param report_type: 报表类型,目前支持日报'day',月报'month',及自定义日期区间的报表
        :param start_date: 日期区间的开始日期,需自定义日期报表时指定
        :param end_date: 日期区间的结束日期,需自定义日期报表时指定
        :return: True/False
        """
        start_date = time.get_last_month_date(time.get_current_date())[0]
        end_date = time.date_add(time.get_current_date(), -1)
        # 多条件筛选
        self._operator_period_control(num)
        self._operator_time_control(start_date, end_date)
        self._operator_point_control()
        # 取数
        self.web_driver.find_element_in_xpath('').text

        return True

    def operation_data_process(self):
        return True

    def operation_data_input(self):
        return True

    def operation_data_backup(self):
        return True

    # def operation_page(self):
    #     param_time = None
    #     time.sleep(1.1)
    #     if not self._operator_time_control(param_time):
    #         logging.error('XXX 异常')
    #         self.error = ErrorEnum.ERROR_1001
    #         return False
    #     return True


class SpreadReportMonth():
    pass