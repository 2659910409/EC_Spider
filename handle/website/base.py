from handle.common.db import DB
from handle.err_message import ErrorEnum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from handle.common import time
import os
import re
import zipfile
import shutil
from timeout3 import timeout
from service.store_service import StoreService
from service.page_data_service import PageDataService


class Base:
    def __init__(self, store_id, data_page_id, port):
        """
        初始化爬虫任务所需的任务信息
        :param data_page:
        :param port:
        :param default_field: 默认添加的字段的值列表
        """
        self.store = StoreService.get_store(store_id)
        self.data_page = PageDataService.get_page_data(data_page_id)
        self.port = port
        self.web_driver = None
        self.source_data = None
        self.data = None
        self.file = None
        self.error = None
        self.default_field = default_field
        self.url = None

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
            print('无法接管端口为{}的浏览器'.format(self.port))
            return False
        return True

    def wait_download(self, cache_path):
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
            dirs = os.listdir(cache_path)
            for filename in dirs:
                print(ind, 'wait_download file:', filename)
                if os.path.isfile(cache_path + filename):
                    file_cnt = file_cnt + 1
                    if '.crdownload' in filename or '.tmp' in filename:
                        atton = True
                        time.sleep(2)
            if file_cnt == 0:
                atton = True
                time.sleep(2)
        return atton

    def is_download_finish(self, cache_path):
        """
        判断文件是否下载完成
        :param cache_path: <class 'str'> 缓存路径
        :return:文件名和文件路径
        """
        self.wait_download(cache_path)
        print('wait_download:', cache_path, ' ok!')
        time.sleep(0.2)
        ls = os.listdir(cache_path)
        length = 0
        for i in ls:
            if os.path.isfile(os.path.join(cache_path, i)):
                cache_file_name = i
                cache_file_path = os.path.join(cache_path, i)
                length = length + 1
        print(ls)
        if len == 1 and '计划日' in cache_file_name:
            # 如果下载的文件为压缩文件,先进行解压,再将压缩包移入备份目录中,只保留解压出的文件
            if re.search(r'\.([^\.]*?)$', cache_file_path).group(1) == 'zip':
                status = self.wait_unzip_finish(cache_path, cache_file_path)
                if status:
                    if self.operation_data_backup(cache_file_path):
                        cache_file_path = os.listdir(cache_path)[0]
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

    def operation_data_backup(self, cache_file_path):
        """
        目前只针对下载文件 进行数据备份
        :return: True/False
        """
        backup_dir = 'D:/' + self.data + '/' + self.port  # 目录规则:平台名-菜单名-页面名-模块名-报表类型
        if os.path.exists(backup_dir):
            print('该目录已存在')
        else:
            os.makedirs(backup_dir)
        shutil.move(cache_file_path, self.backup_dir)
        return True

