from handle.website.base import Base
from handle.err_message import ErrorEnum
from handle.common import logging
from handle.common import time
from handle.common import db
from retry import retry
import pandas as pd
import re

class SpreadReport(Base):
    def _operator_time_control(self, start_date=None, end_date=None):
        """
        时间筛选控件操作
        :param start_date: 日期区间的开始日期,需自定义日期报表时指定
        :param end_date: 日期区间的结束日期,需自定义日期报表时指定
        :return: True/False
        """
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').send_keys(time.date_to_string(start_date))
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').send_keys(time.date_to_string(end_date))
        self.web_driver.find_element_in_xpath('//*[@id="mx_423"]').click()


    def _operator_period_control(self, period):
        """
        转化周期控件操作
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
        定位到指定取数的页面
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

    def operation_data_process(self):
        return True

    def operation_data_input(self):
        return True

    def operation_data_backup(self):
        return True
    pass


class SpreadReportDay(SubReport):
    @retry(tries=3, delay=2)
    def operation_page(self):
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
        self._operator_period_control(self.period)
        self._operator_time_control(start_date, end_date)
        self._operator_point_control()
        # 取数
        self.web_driver.find_element_in_xpath('').text

        return True

    def operation_data_process(self):
        """
        下载文件并解析文件数据
        :return:
        """
        db_conn, db_cur = db.create_conn()
        file_path = self.is_download_finish()
        db_cur.execute(
            "select column_name from information_schema.columns where table_name = {} and table_schema = {};").format(self.table_name, self.db_name)
        field_name = db_cur.fetchall()
        field_name_list = []
        for x in field_name:
            field_name_list.append(x[0])
        data_sheets = pd.read_excel(cache_file_path, None)
        sheets_name = list(data_sheets.keys())
        df = data_sheets[sheets_name[0]]
        # 添加默认字段并赋值
        df = pd.concat([df, pd.DataFrame(columns=self.FIELD_NAME)], sort=False)
        df['店铺id'] = '3'
        df['店铺名'] = '皇家美素佳儿旗舰店'
        df['入库时间'] = datetime.datetime.now()
        df['取数时间'] = datetime.datetime.now()
        row_cnt = df.shape[0]
        col_cnt = df.shape[1]
        if row_cnt <= 0 or col_cnt <= 0:  # 需要判断表格中是否存在业务数据
            pass
        cols_name = df.columns.tolist()
        for col_name in cols_name:
            col_name_new = re.sub(r'[\(\)]', '_', re.sub(r'\(%\)', '', col_name))
            df.rename(columns={col_name: col_name_new}, inplace=True)
        cols_name_new = df.columns.tolist()
        increase_field = list(set(cols_name_new) - set(field_name_list))
        reduce_field = list(set(field_name_list) - set(cols_name_new))
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
    @retry(tries=3, delay=2)
    def operation_page(self):
        """
        :param url: 指定抓取页面的url
        :param num: 转化周期筛选
        :param report_type: 报表类型,目前支持日报'day',月报'month',及自定义日期区间的报表
        :param start_date: 日期区间的开始日期,需自定义日期报表时指定
        :param end_date: 日期区间的结束日期,需自定义日期报表时指定
        :return: True/False
        """
        symbol = False
        start_date = time.get_last_month_date(time.get_current_date())[0]
        end_date = time.date_add(time.get_current_date(), -1)
        # 多条件筛选
        self._operator_period_control(self.period)
        self._operator_time_control(start_date, end_date)
        self._operator_point_control()
        # 取数
        self.web_driver.find_element_in_xpath('').text
        symbol = True
        return symbol