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

    def _locate_page(self):
        """
        定位到指定取数的页面
        :param url: 指定抓取页面的url
        :return: True/False
        """
        try:
            self.web_driver.get(self.url) # 第一次请求到达平台默认页
            self.web_driver.close(self.url)
            self.web_driver.get(self.url)  # 第二次请求是为了到达指定的爬虫页
        except as e:
            print(e, '请求失败,请检查传入的url是否有效:{}'.format(self.url))
            return False
        return True


class SpreadReportDay(SpreadReport):
    @retry(tries=3, delay=2)
    def operation_page(self):
        """
        报表条件筛选并下载报表
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
        等待文件下载完成并解析文件数据
        :return: data_frame
        """
        # 从数据库读取目标表的所有字段名
        db_conn, db_cur = db.create_conn()
        db_cur.execute(
            "select column_name from information_schema.columns where table_name = {} and table_schema = {};").format(
            self.table_name, self.db_name)
        field_name = db_cur.fetchall()
        field_name_list = []
        for x in field_name:
            field_name_list.append(x[0])
        field_name_list.sort(reverse=True)
        field_tuple = tuple(field_name_list)
        # 读取文件并解析
        cache_file_name, cache_file_path = self.is_download_finish()
        df = pd.read_csv(cache_file_path)
        if df.shape[0] <= 0 or df.shape[1] <= 0:  # 需要判断表格中是否存在业务数据
            print('下载的文件为空文件')
        # 添加默认字段并赋值
        df = pd.concat([df, pd.DataFrame(columns=self.FIELD_NAME)], sort=False)
        df['店铺id'] = self.store_id
        df['店铺名'] = self.store_name
        df['入库时间'] = time.get_current_timestamp()
        df['取数时间'] = time.get_current_timestamp()
        cols_name = df.columns.tolist()
        # 将不符合命名规则的字段名重命名
        for col_name in cols_name:
            col_name_new = re.sub(r'[\(\)]', '_', re.sub(r'\(%\)', '', col_name))
            df.rename(columns={col_name: col_name_new}, inplace=True)
        cols_name_new = df.columns.tolist()
        # 比较文件数据中的字段与数据库表中字段的差异
        increase_field = list(set(cols_name_new) - set(field_name_list)) # 多出的字段需处理到告警信息中
        reduce_field = list(set(field_name_list) - set(cols_name_new))
        # 如果文件数据中的字段有减少,需要添加该字段,默认将该字段列赋空值
        if reduce_field:
            df = pd.concat([df, pd.DataFrame(columns=reduce_field)], sort=False)
        df = df[field_name_list].sort_index(axis=1, ascending=False) # 将数据列按照列名降序排序
        return field_tuple, df


    def operation_data_input(self, field_tuple, df):
        """
        将读取到的data_frame按照字段名写入到数据库
        :param field_tuple: 表字段名组成的元组
        :param df: 读取到的data_frame
        :return: True/False
        """
        # row_cnt = df.shape[0]
        col_cnt = df.shape[1] # 取出data_frame列数
        data_list = list(df.itertuples(index=False, name=None)) # 将data_frame每一行转化为元组放入列表中
        insert_sql = "insert into {} {} values (%s{})".format(self.table_name, field_tuple, ',%s'*(col_cnt-1))
        db_cur.executemany(insert_sql, data_list)
        db_conn.commit()

    def run(self):
        self.get_webdriver()
        self._locate_page()

        pass


class SpreadReportMonth(SpreadReport):
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