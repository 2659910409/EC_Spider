# -*- coding: utf-8 -*-
from common.db import DB
from handle.err_message import ErrorEnum
from common.private_logging import Logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from handle.common import time
import os
import shutil
import zipfile
import pandas as pd
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
            # TODO 需支持指定下载目录:self.store.name/self.page_data.name
            self.FILE_DOWNLOAD_PATH = setting.FILE_DOWNLOAD_PATH_PREFIX+'/'+self.store.name
            self.FILE_PROCESS_PATH = setting.FILE_PROCESS_PATH_PREFIX+'/'+self.store.name+'/'+self.page_data.name+'/'+self.page_data.data_update_freq
            self.FILE_BACKUP_PATH = setting.FILE_BACKUP_PATH_PREFIX+'/'+self.store.name+'/'+self.page_data.name+'/'+self.page_data.data_update_freq
            if not os.path.exists(self.FILE_DOWNLOAD_PATH):
                os.makedirs(self.FILE_DOWNLOAD_PATH)
            if not os.path.exists(self.FILE_PROCESS_PATH):
                os.makedirs(self.FILE_PROCESS_PATH)
            if not os.path.exists(self.FILE_BACKUP_PATH):
                os.makedirs(self.FILE_BACKUP_PATH)
            # 下载目录清理
            # TODO 可配置变量
            file_prefix = ''
            self.clear_download_path(file_prefix)
            self.web_driver = None
            # 下载文件取数时需要
            # TODO 数据列表定义
            self.file_names = []
            self.source_data_list = []
            self.data_list = []
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_1000

    def get_file_names(self):
        if len(self.file_names) == 0:
            raise Exception('文件列表未下载或不存在')
        return self.file_names

    def get_file_name(self):
        if len(self.file_names) == 1:
            return self.file_names[0]
        elif len(self.file_names) > 1:
            raise Exception('文件使用错误，非单个文件下载')
        else:
            raise Exception('文件未下载或不存在')

    def get_source_data_list(self):
        if len(self.source_data_list) == 0:
            raise Exception('原始数据不存在')
        return self.source_data_list[0]

    def get_source_data(self):
        if len(self.source_data_list) == 1:
            return self.source_data_list[0]
        elif len(self.source_data_list) > 1:
            raise Exception('原始数据使用错误，原始数据为列表数据')
        else:
            raise Exception('原始数据不存在')

    def get_data_list(self):
        if len(self.data_list) == 0:
            raise Exception('原始数据不存在')
        return self.data_list[0]

    def get_data(self):
        if len(self.data_list) == 1:
            return self.data_list[0]
        elif len(self.data_list) > 1:
            raise Exception('数据使用错误，数据为列表数据')
        else:
            raise Exception('数据不存在')

    def operation_page(self):
        """
        页面操作含取数，获取：self.source_data/self.file_names
        1) 页面操作
        2）是否有文件下载 TODO page_data 逻辑控制
        3）文件是否下载完成
        4）文件下载完成后迁移
        5）读取文件内容返回数据,读取文件内容存储：self.source_datas
        :return: True/False
        """
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
        目前只针对下载文件 进行数据备份（针对文件下载类取数）
        :return: True/False
        """
        # TODO self.file_process_path_suffix 文件目录规则
        for file_name in self.get_file_names():
            if self.self.file_process_path_suffix is None:
                shutil.move(os.path.join(self.FILE_PROCESS_PATH, file_name), os.path.join(self.FILE_BACKUP_PATH, file_name))
                print("move %s -> %s" % (os.path.join(self.FILE_PROCESS_PATH, file_name), os.path.join(self.FILE_BACKUP_PATH, file_name)))
            else:
                process_path = self.FILE_PROCESS_PATH + '/' + str(self.file_path_suffix)
                backup_path = self.FILE_BACKUP_PATH + '/' + str(self.file_path_suffix)
                if not os.path.exists(process_path):
                    os.makedirs(process_path)
                if not os.path.exists(backup_path):
                    os.makedirs(backup_path)
                shutil.move(os.path.join(process_path, file_name), os.path.join(backup_path, file_name))
                print("move %s -> %s" % (os.path.join(process_path, file_name), os.path.join(backup_path, file_name)))
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

    def clear_download_path(self, file_prefix=None):
        """
        按文件前缀规则清理目录
        :param file_prefix:
        :return:
        """
        # 未配置下载文件名规则，清空下载目录中的文件
        files = os.listdir(self.FILE_DOWNLOAD_PATH)
        for file in files:
            file_path = os.path.join(self.FILE_DOWNLOAD_PATH, file)
            if os.path.isfile(file_path):
                if file_prefix is None or file.find(file_prefix) == 0:
                    # TODO 文件做备份,规则？
                    os.remove(file_path)
                    print('清空文件夹 remove:', file_path)

    def wait_download_finish(self, file_prefix=None, file_path_suffix=None):
        """
        根据文件前缀规则匹配，文件是否下载完成
        :param file_prefix:
        :return:
        """
        timeout_num = 180 # 文件下载超时3分组
        _file_name = None
        while timeout_num >= 0:
            files = os.listdir(self.FILE_DOWNLOAD_PATH)
            for file in files:
                file_path = os.path.join(self.FILE_DOWNLOAD_PATH, file)
                # 文件下载中，文件后缀
                if '.crdownload' in file or '.tmp' in file:
                    time.sleep(1)
                    timeout_num = timeout_num - 1
                    continue
                # 匹配到的文件数量
                match_file_cnt = 0
                if file_prefix is None and os.path.isfile(file_path):
                    match_file_cnt = match_file_cnt+1
                    _file_name = file
                elif file.find(file_prefix) == 0 and os.path.isfile(file_path):
                    match_file_cnt = match_file_cnt + 1
                    _file_name = file
                if match_file_cnt == 0:
                    time.sleep(1)
                    timeout_num = timeout_num - 1
                    continue
                elif match_file_cnt == 1:
                    self.file_names.append(file)
                    # 将文件移到处理目录
                    # TODO 指定存储文件目录规则
                    if file_path_suffix is None:
                        file_process_path = self.FILE_PROCESS_PATH
                    else:
                        self.file_path_suffix = str(file_path_suffix) # TODO 配置
                        file_process_path = self.FILE_PROCESS_PATH+'/'+str(file_path_suffix)
                        if not os.path.exists(file_process_path):
                            os.makedirs(file_process_path)
                    remote_path = os.path.join(file_process_path, file)
                    # TODO 目标文件已存在备份？
                    if not os.path.exists(remote_path):
                        os.remove(remote_path)
                    shutil.move(file_path, remote_path)  # 移动文件
                    print("move %s -> %s" % (file_path, remote_path))
                    # TODO 当前写死，通用需要文件类型配置
                    self.source_data_list.append(pd.read_excel(remote_path))
                    return True
                else:
                    raise Exception('文件未匹配')
        return False

    def unzip(self, cache_path, cache_file_path):
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
