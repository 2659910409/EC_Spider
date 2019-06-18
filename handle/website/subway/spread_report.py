from handle.website.base import Base
from handle.err_message import ErrorEnum
from common.private_logging import Logging
from retry import retry
import pandas as pd
from service.page_data_service import PageDataService
from handle.common.private_time import *


class SpreadReport(Base):
    def _operator_time_control(self, start_date=None, end_date=None):
        """
        时间筛选控件操作
        :param start_date: 日期区间的开始日期,需自定义日期报表时指定
        :param end_date: 日期区间的结束日期,需自定义日期报表时指定
        """
        # 获取日期控件文本框并输入日期
        self.web_driver.find_element_in_xpath('//*[@id="mx_1485"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="mx_1485"]').send_keys(date_to_string(start_date))
        self.web_driver.find_element_in_xpath('//*[@id="mx_1486"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="mx_1486"]').send_keys(date_to_string(end_date))
        # 点击确定
        self.web_driver.find_element_in_xpath('//*[@id="brix_6985"]/ div/div/div[2]/a[1]').click()
        self.web_driver.find_element_in_xpath('//*[@id="J_bpreport_dpanel_mx_1465"]/form/div/a[1]').click()

    def _operator_name_control(self):
        """操作报表名称文本框"""
        file_name = self.page_data.name + date_to_string(get_current_timestamp(), '%Y%m%d%H%M%S')
        self.web_driver.find_element_in_xpath('//*[@id="J_bpreport_dname_mx_1465"]').clear()
        self.web_driver.find_element_in_xpath('//*[@id="J_bpreport_dname_mx_1465"]').send_keys(file_name)
        self.web_driver.find_element_in_xpath('//*[@id="brix_brick_6587"]/ul/li[1]').click()

    def _locate_page(self):
        """
        定位到指定取数的页面
        :param url: 指定抓取页面的url
        :return: True/False
        """
        try:
            self.web_driver.get(self.page.url)  # 第一次请求到达平台默认页
            self.web_driver.close(self.page.url)
            self.web_driver.get(self.page.url)  # 第二次请求是为了到达指定的爬虫页
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_3001
            return False
        return True


class SpreadReportBabyDay(SpreadReport):
    def operation_page(self):
        """
        报表条件筛选
        """
        try:
            start_date, end_date = get_day_report_rule1()
            # 各控件筛选操作
            self._operator_name_control()
            self._operator_time_control(start_date, end_date)
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_3002
            return False
        return True

    def operation_page_download(self):
        """
        下载报表,并读取数据
        """
        # 读取文件并解析
        # 等待 todo
        download_url = 'https://subway.simba.taobao.com/#!/report/bpreport/download'
        self.web_driver.get(download_url)
        # 获取总页数
        page_num = self.web_driver.find_element_in_xpath('//*[@id="brix_brick_291"]/div[2]/div[2]/span[2]').text
        for x in range(page_num):
            download_url = 'https://subway.simba.taobao.com/#!/report/bpreport/download' + '?page={}'.format(x)
            self.web_driver.get(download_url)
            if self.web_driver.find_element_in_xpath(''):
                self.web_driver.find_element_in_xpath('').click()
                break
        self.wait_download_finish()

    def operation_data_process(self):
        """
        等待文件下载完成并解析文件数据
        :return: data_frame
        """
        try:
            # 从数据库读取目标表的所有字段名
            check_field_names = []  # 存储需要进行比对的字段名
            db_field_names = []  # 存储数据库中表的所有字段名
            default_add_field = []  # 存储默认需要添加的字段名
            for data_tab_column in self.page_data.data_tabs[0].data_tab_columns:
                if data_tab_column.check_col_name is not None:
                    check_field_names.append(data_tab_column.check_col_name)
                if data_tab_column.check_col_name is None:
                    default_add_field.append(data_tab_column.col_name)
                db_field_names.append(data_tab_column.col_name)
            # check_field_names.sort(reverse=True)
            # 添加默认字段并赋值
            df = self.source_data_list[0]  # 取出读取到的data_frame
            df = pd.concat([df, pd.DataFrame(columns=self.default_add_field)], sort=False)
            df['店铺id'] = self.store.id
            df['店铺名'] = self.store.name
            df['日期'] = df['_日期']
            df['文件路径'] = self.FILE_BACKUP_PATH
            df['文件sheet'] = 'sheet'
            df['转化周期'] = '15天累计数据'
            df['报表类型'] = '宝贝'
            df['入库时间'] = get_current_timestamp()
            df['取数时间'] = get_current_timestamp()
            file_col_names = df.columns.tolist()
            # 比较文件数据中的字段与数据库表中字段的差异
            increase_field = list(set(file_col_names) - set(check_field_names))  # 多出的字段需处理到告警信息中
            reduce_field = list(set(check_field_names) - set(file_col_names))
            self.data_list.append(df)
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_5001
            return False
        return True

    def operation_data_input(self):
        """
        将读取到的data_frame按照字段名写入到数据库
        :param field_tuple: 表字段名组成的元组
        :param df: 读取到的data_frame
        :return: True/False
        """
        try:
            df = self.data
            field_tuple = PageDataService.get_file_columns(self.page_data)
            # row_cnt = df.shape[0]
            col_cnt = df.shape[1]  # 取出data_frame列数
            data_list = list(df.itertuples(index=False, name=None))  # 将data_frame每一行转化为元组放入列表中
            insert_sql = "insert into {} {} values (%s{})".format(self.page_data.data_tabs[0].name, field_tuple, ',%s'*(col_cnt-1))
            self.db.insert_many(insert_sql, data_list)
            self.db.commit()
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_5002

    # def run(self):
    #     self.get_webdriver()
    #     self._locate_page()
    #     self.operation_page()
    #     field_tuple, df = self.operation_data_process()
    #     self.operation_data_input(field_tuple, df)
    #     self.operation_data_backup()


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