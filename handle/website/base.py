# -*- coding: utf-8 -*-
from common.db import DataBase
from handle.err_message import ErrorEnum
from common.private_logging import Logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from common.private_time import Time
import os
import shutil
import zipfile
import pandas as pd
from service.store_service import StoreService
from service.page_data_service import PageDataService
import setting
from entity.page_data import DataTabEntity


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
            self.db = DataBase()
            self.port = port
            self.FILE_PART_PATH = self.store.name+'/'+self.page_data.name+'/'+self.page_data.data_update_freq
            self.FILE_DOWNLOAD_PATH = setting.FILE_DOWNLOAD_PATH_PREFIX+'/'+self.store.name
            self.FILE_PROCESS_PATH = setting.FILE_PROCESS_PATH_PREFIX+'/'+self.FILE_PART_PATH
            self.FILE_BACKUP_PATH = setting.FILE_BACKUP_PATH_PREFIX+'/'+self.FILE_PART_PATH
            if not os.path.exists(self.FILE_DOWNLOAD_PATH):
                os.makedirs(self.FILE_DOWNLOAD_PATH)
            if not os.path.exists(self.FILE_PROCESS_PATH):
                os.makedirs(self.FILE_PROCESS_PATH)
            if not os.path.exists(self.FILE_BACKUP_PATH):
                os.makedirs(self.FILE_BACKUP_PATH)
            # 下载目录清理
            self.clear_download_path()
            # 初始化webdriver，判断是否已登录
            self.driver = None
            self.init_web_driver()
            self.check_store_login()
            # 数据维度字典
            self.data_dimension_dict = {}
            # 下载文件取数时需要
            self.file_names = []
            # 单文件、单数据表存储，例：[DataFrame]
            # 多文件/多sheet、单数据表存储，例：[DataFrame, DataFrame, DataFrame] # TODO 暂无忽略
            # 多文件/多sheet、多数据表存储：判断条件 page_data.is_multiple_tab()
            # 例：[{'tab.name', [DataFrame]}, {'tab.name', [DataFrame, DataFrame]}]
            self.source_data_list = []
            self.data_list = []
        except Exception as e:
            Logging.error(e)
            self.error = ErrorEnum.ERROR_1000

    def get_file_path_effective(self):
        return self.FILE_PROCESS_PATH.replace(setting.FILE_PROCESS_PATH_PREFIX)

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
        2）是否有文件下载
        3）文件是否下载完成
        4）文件下载完成后迁移
        5）读取文件内容返回数据,读取文件内容存储：self.source_data_list
        :return: True/False
        """
        return True

    def operation_data_process(self):
        """
        数据处理
        1） 数据格式转换
        2） 数据列类型转换:self.data_list
        :return: True/False
        """
        # self.data_list = self.source_data_list
        return True

    def operation_data_input(self):
        """
        数据入库
        :return: True/False
        """
        # DataBase.input_batch(self.data)
        return True

    def operation_data_backup(self):
        """
        目前只针对下载文件 进行数据备份（针对文件下载类取数）
        :return: True/False
        """
        if not self.page_data.is_file_download():
            return True
        for file_name in self.get_file_names():
            # 存在特殊目录规则时 rule_save_path_suffix 不为空，目录后缀增加该规则
            path_suffix = self.page_data.rule_save_path_suffix
            if path_suffix is None:
                shutil.move(os.path.join(self.FILE_PROCESS_PATH, file_name), os.path.join(self.FILE_BACKUP_PATH, file_name))
                print("move %s -> %s" % (os.path.join(self.FILE_PROCESS_PATH, file_name), os.path.join(self.FILE_BACKUP_PATH, file_name)))
            else:
                for key in self.data_dimension_dict.keys():
                    path_suffix = path_suffix.replace(key, self.data_dimension_dict[key])
                process_path = self.FILE_PROCESS_PATH + '/' + path_suffix
                backup_path = self.FILE_BACKUP_PATH + '/' + path_suffix
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

    def init_web_driver(self):
        """
        根据端口获取浏览器driver
        :return: True/False
        """
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(self.port))
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

            Logging.info('{} - Chrome[{}]连接成功。'.format(self.store.name, self.port))
        except Exception as e:
            print(e)
            Logging.error('port:{} 无法接管浏览器'.format(self.port))
            self.error = ErrorEnum.ERROR_1003
            raise Exception
        return True

    def check_store_login(self):
        self.driver.get('https://sycm.taobao.com')
        Time.sleep(1)
        current_url = self.driver.current_url
        if 'login.htm' in current_url:
            Logging.error('store:', self.store.name, 'current_url:', current_url, '店铺未登录，无法继续取数！')
            self.error = ErrorEnum.ERROR_1004
            raise Exception('store:', self.store.name, '店铺未登录，无法继续取数！')
        self.login_flag = Time

    def clear_download_path(self):
        """
        按文件前缀规则清理目录
        :return:
        """
        # 未配置下载文件名规则，清空下载目录中的文件
        files = os.listdir(self.FILE_DOWNLOAD_PATH)
        for file in files:
            file_path = os.path.join(self.FILE_DOWNLOAD_PATH, file)
            if os.path.isfile(file_path):
                if self.page_data.rule_read_file_prefix is None or file.find(self.page_data.rule_read_file_prefix) == 0:
                    # TODO 文件做备份,时间戳.原文件名
                    os.remove(file_path)
                    print('清空文件夹 remove:', file_path)

    def wait_download_finish(self, file_type=None):
        """
        根据文件前缀规则匹配，文件是否下载完成
        :param file_type:
        :return:
        """
        # 文件下载超时3分钟
        timeout_num = 180
        while timeout_num >= 0:
            # 匹配到的文件数量
            match_file_cnt = 0
            files = os.listdir(self.FILE_DOWNLOAD_PATH)
            for file in files:
                file_path = os.path.join(self.FILE_DOWNLOAD_PATH, file)
                # 文件下载中，文件后缀
                if '.crdownload' in file or '.tmp' in file:
                    Time.sleep(1)
                    timeout_num = timeout_num - 1
                    continue
                match_file_cnt = 0
                if self.page_data.rule_read_file_prefix is None and os.path.isfile(file_path):
                    match_file_cnt = match_file_cnt+1
                elif file.find(self.page_data.rule_read_file_prefix) == 0 and os.path.isfile(file_path):
                    match_file_cnt = match_file_cnt + 1
            if match_file_cnt == 0:
                Time.sleep(1)
                timeout_num = timeout_num - 1
                continue
            elif match_file_cnt == 1:
                self.file_names.append(file)
                # 将文件移到处理目录
                if self.page_data.rule_save_path_suffix is None:
                    file_process_path = self.FILE_PROCESS_PATH
                else:
                    path_suffix = self.page_data.rule_save_path_suffix
                    for key in self.data_dimension_dict.keys():
                        path_suffix = path_suffix.replace(key, self.data_dimension_dict[key])
                    file_process_path = self.FILE_PROCESS_PATH+'/'+path_suffix
                    if not os.path.exists(file_process_path):
                        os.makedirs(file_process_path)
                remote_path = os.path.join(file_process_path, file)
                # TODO 目标文件已存在文件需重命名，时间戳.原文件名
                if os.path.exists(remote_path):
                    os.remove(remote_path)
                shutil.move(file_path, remote_path)  # 移动文件
                Logging.info("move %s -> %s" % (file_path, remote_path))
                # 文件读取
                # TODO 解压文件操作，多文件、多sheet操作
                # TODO 通用需要文件类型配置，常规文件类型支持
                if file_type is None:
                    if file[-3:] == 'csv':
                        file_type = 'csv'
                    elif file[-3:] == 'xls' or file[-4:] == 'xlsx':
                        file_type = 'excel'
                if file_type == 'excel':
                    df = pd.read_excel(remote_path)
                elif file_type == 'csv':
                    df = pd.read_csv(remote_path)
                else:
                    Logging.error('解析文件类型，未找到！')
                    raise Exception('解析文件类型，未找到！')
                self.source_data_list.append(df)
                return True
            else:
                raise Exception('文件下载失败')
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

    def str_to_char(self, string):
        """
        字符串转字符
        :param string:
        :return:
        """
        _string = str(string)
        if not _string:
            return ''
        _string = _string.strip()
        if _string == '' or _string == '-':
            return ''
        return _string

    def str_to_int(self, string):
        """
        字符串转整型
        :param string:
        :return: int类型
        """
        _string = str(string)
        if not _string:
            return 0
        _string = _string.strip()
        _string = _string.replace(',', '')
        if _string.strip() == '' or _string.strip() == '-':
            return 0
        if '%' in _string:
            _string = _string.replace('%', '')
            _string = round(int(_string) / 100)
        return int(_string)

    def str_to_float(self, string):
        """
        字符串转浮点型
        :param string:
        :return: float类型
        """
        _string = str(string)
        if not _string:
            return 0.0
        _string = _string.strip()
        _string = _string.replace(',', '')
        if _string.strip() == '' or _string.strip() == '-':
            return 0.0
        if '%' in _string:
            _string = _string.replace('%', '')
            _string = round(float(_string) / 100)
        return float(_string)

    def df_effective_by_starting_position(self, starting_position, source_df: pd.DataFrame):
        """
        根据启始位置，获取有效数据
        :param starting_position: 起始位置
        :param source_df: 原始数据
        :return: DataFrame
        """
        get_data_flag = False
        data_cols = None  # 数据表title
        data_list = []  # 数据表内容
        for index, row in source_df.T.iteritems():
            values = row.values
            if get_data_flag:
                data_list.append(values)
            if values[0] == starting_position:
                get_data_flag = True
                data_cols = values
        if len(data_list) == 0:
            Logging.warning('无数据！')
            return True
        df = pd.DataFrame(data_list, columns=data_cols)
        return df

    def df_data_process(self, data_tab: DataTabEntity, df: pd.DataFrame):
        """
        取所需数据列，数据类型转换
        :param data_tab: 数据表配置
        :param df: 待数据数据DataFrame
        :return: DataFrame
        """
        conf_columns = data_tab.get_file_columns()
        conf_check_columns = data_tab.get_file_check_columns()
        intersection_col = []
        data_col_ind = []
        # for col in conf_check_columns:
        #     if col in data_cols:
        #         data_col_ind.append(data_cols.index(col))
        #         intersection_col.append(col)
        # for d in data_list:
        #     _row = []
        #     for ind in data_col_ind:
        #         col_name = intersection_col[ind]
        #         col_val = d[ind]
        #         if col_name in ['int', 'bigint', 'int32', 'int64', 'tinyint', 'integer']:
        #             _col_val = self.str_to_int(col_val)
        #         elif col_name in ['float', 'numeric', 'decimal', 'double']:
        #             _col_val = self.str_to_float(col_val)
        #         elif col_name in ['varchar', 'string']:
        #             _col_val = self.str_to_int(col_val)
        #         else:
        #             _col_val = col_val
        #         _row.append(_col_val)
        #     _data.append(_row)
        # # 数据列校验, TODO 监控告警
        # tmp_surplus = list(set(data_cols) - set(conf_columns))  # 新增字段/列
        # tmp_defect = list(set(conf_columns) - set(data_cols))  # 缺少字段/列
        # Logging.warning('字段列匹配，原始字段列表：', data_cols) if len(tmp_surplus + tmp_defect) > 0 else None
        # Logging.warning('字段列匹配，配置字段列表：', conf_columns) if len(tmp_surplus + tmp_defect) > 0 else None
        # Logging.warning('字段列匹配，新增字段/列：', tmp_surplus) if len(tmp_surplus) > 0 else None
        # Logging.warning('字段列匹配，缺少字段/列：', tmp_defect) if len(tmp_defect) > 0 else None
        # # DataFrame生成
        # import pandas as pd
        # df = pd.DataFrame(_data, columns=intersection_col)
        return df

    def gen_data_maintenane_condition(self, tab: DataTabEntity, df: pd.DataFrame):
        """
        根据配置与数据，生成数据维护条件
        :param tab:
        :param df:
        :return:
        """
        return ''

    def gen_data_insert_values(self, tab: DataTabEntity, df: pd.DataFrame):
        """

        :param tab:
        :param df:
        :return:
        """
        return ''
