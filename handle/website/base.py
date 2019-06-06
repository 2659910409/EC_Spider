from handle.common.db import DB
from handle.err_message import ErrorEnum


class Base:
    def __init__(self, store, data_page, port):
        self.store = store
        self.data_page = data_page
        self.port = port
        self.webdriver = None
        self.source_data = None
        self.data = None
        self.file = None
        self.error = None


    def get_webdriver(self):
        """
        根据端口获取浏览器
        :param port:
        :return: True/False
        """
        self.webdriver = None
        return True

    def operation_page(self):
        """
        页面操作含取数
        :return: True/False
        """
        self.source_data = None
        return True

    def operation_page_download(self):
        """
        文件下载及下载文件管理
        1）是否有文件下载
        2）文件是否下载完成
        3）文件下载完成后迁移
        4）读取文件内容返回数据
        :return: True/False
        """
        self.file = None
        self.source_data = None
        return True

    def operation_data_process(self):
        """
        数据处理
        1） 数据格式转换
        2） 数据列类型转换
        :return: True/False
        """
        self.data = self.source_data
        return True

    def operation_data_input(self):
        """
        数据入库
        :return: True/False
        """
        DB.input_batch(self.data)
        return True

    def operation_data_backup(self):
        """
        目前只针对下载文件 进行数据备份
        :return: True/False
        """
        self.file
        return True
