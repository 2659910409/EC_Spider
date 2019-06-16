# -*- coding: utf-8 -*-
from common.db import DB
from handle.err_message import ErrorEnum
from common.private_logging import Logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from handle.common import time
import os
import re
import zipfile
import shutil
from service.store_service import StoreService
from service.page_data_service import PageDataService
import setting


class Base:

    def __init__(self, store_id, page_data_id, port):
        """
        初始化爬虫任务所需的信息
        1.实例化对象：Store、PageData、Table
        2.环境初始化
        3.web_driver 连接确认
        4.web_driver 店铺LOGIN确认，确认浏览正常并店铺已登录成功时置login_flag=True
        :param store_id: 店铺id,用来获取店铺对象
        :param page_data_id: 抓取的页面数据块id,用来获取页面数据块对象
        :param port: 已开启的浏览器服务端口
        """
        self.error = None
        self.login_flag = False
        try:
            self.store = StoreService().get_store(store_id)
            self.page_data = PageDataService().get_page_data(page_data_id)
            self.page = self.page_data.page
            self.db = DB()
            self.port = port
            self.cache_path = setting.DATA_ROOT_PATH
            self.web_driver = None
            self.file = None
            self.source_data = None
            self.data = None
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_1000

    def operation_page(self):
        """
        页面操作含取数
        :return: True/False
        """
        self.source_data = None
        return True

    def operation_page_download(self):
        """
        文件下载及下载文件管理（针对文件下载类取数）
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

    def operation_data_backup(self, cache_file_path):
        """
        目前只针对下载文件 进行数据备份（针对文件下载类取数）
        :return: True/False
        """
        # TODO 根路径引用
        backup_dir = 'C:/RPA DATA/' + self.data + '/' + self.port  # 目录规则:平台名-菜单名-页面名-模块名-报表类型
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        shutil.move(cache_file_path, self.backup_dir)
        return True

    def is_success(self):
        if self.error is None:
            return True
        return False

    def get_error(self):
        return self.error.value

    def set_error_msg(self, msg):
        self.error.value.set_msg(msg)

    def get_webdriver(self):
        """
        根据端口获取浏览器
        :return: True/False
        """
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(self.port))
            self.web_driver = webdriver.Chrome(chrome_options=chrome_options)
        except Exception as e:
            Logging('无法接管端口为{}的浏览器'.format(self.port))
            self.error = ErrorEnum.ERROR_1000

    def wait_download(self):
        """
        等待文件下载
        :param cache_path:
        :return:
        """
        atton = True
        # timeout配置
        ind = 0
        while atton:
            ind = ind + 1
            atton = False
            file_cnt = 0
            dirs = os.listdir(self.cache_path)
            for filename in dirs:
                print(ind, 'wait_download file:', filename)
                if os.path.isfile(self.cache_path + filename):
                    file_cnt = file_cnt + 1
                    if '.crdownload' in filename or '.tmp' in filename:
                        atton = True
                        time.sleep(2)
            if file_cnt == 0:
                atton = True
                time.sleep(2)
        return atton

    def is_download_finish(self):
        """
        判断文件是否下载完成
        :param cache_path: <class 'str'> 缓存路径
        :return:文件名和文件路径
        """
        self.wait_download(self.cache_path)
        print('wait_download:', self.cache_path, ' ok!')
        time.sleep(0.2)
        ls = os.listdir(self.cache_path)
        length = 0
        for i in ls:
            if os.path.isfile(os.path.join(self.cache_path, i)):
                cache_file_name = i
                cache_file_path = os.path.join(self.cache_path, i)
                length = length + 1
        print(ls)
        if len == 1 and '计划日' in cache_file_name:
            # 如果下载的文件为压缩文件,先进行解压,再将压缩包移入备份目录中,只保留解压出的文件
            if re.search(r'\.([^\.]*?)$', cache_file_path).group(1) == 'zip':
                status = self.wait_unzip_finish(self.cache_path, cache_file_path)
                if status:
                    if self.operation_data_backup(cache_file_path):
                        cache_file_path = os.listdir(self.cache_path)[0]
                        return cache_file_name, cache_file_path
            return cache_file_name, cache_file_path
        elif len == 0:
            print('无文件异常，无法处理！')
            raise IOError
        else:
            print('多文件异常，无法处理！')
            raise IOError
        return cache_file_name, cache_file_path

    def wait_unzip_finish(self, cache_path, cache_file_path):
        """
        对压缩文件解压缩
        :param cache_path:
        :param cache_file_path:
        :return: True/False
        """
        symbol = False
        with zipfile.ZipFile(cache_file_path) as zfile:
            zfile.extractall(path=cache_path)
        if len(os.listdir(cache_path)) == 2:
            symbol = True
        elif len(os.listdir(cache_path)) < 2:
            print('文件解压失败')
        else:
            print('解压出多个文件')
        return symbol
