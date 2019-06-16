from dao.page_data_dao import *
from entity.page_data import *
from common.private_logging import Logging


class PageService:
    def get_page(self, page_id):
        """
        获取需要抓取的页面信息
        :param page_id: 页面id
        :return: page实体对象
        """
        data = PageDao().query(page_id)
        if data:
            data = data[0]
            page = PageEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            return page
        else:
            Logging.error('page_id:', page_id, ' 不存在！')

    def add_page(self, website, menu_level_first, url, menu_level_second, menu_level_third):
        """
        增加page
        :param website:
        :param menu_level_first:
        :param url:
        :param menu_level_second:
        :param menu_level_third:
        :return:
        """
        key = PageDao().insert(website, menu_level_first, url, menu_level_second, menu_level_third)
        page = self.get_page(key)
        return page


class PageDataService:
    def get_page_data(self, page_data_id):
        """
        获取页面数据块信息
        :param page_data_id: 页面数据块id
        :return: 页面数据块的实体对象
        """
        data = PageDataDao().query(page_data_id)
        if data:
            data = data[0]
            page_data_confs = self._get_page_data_confs(page_data_id)
            page = PageService().get_page(data[1])
            data_tabs = self._get_data_tabs(page_data_id)
            page_data = PageDataEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], page_data_confs, page, data_tabs)
            return page_data
        else:
            Logging.error('不存在该page_data_id:', page_data_id)
        return None

    def _get_page_data_confs(self, page_data_id):
        data = PageDataConfDao().query_by_page_data_id(page_data_id)
        if data:
            page_data_confs = []
            for row in data:
                page_data_confs.append(PageDataConfEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            return page_data_confs
        else:
            Logging.error('不存在该page_data_id:', page_data_id)

    def add_page_data(self, page_id, data_name, data_source_type, data_update_freq, data_update_time, data_tabs, page_data_confs=None):
        """
        增加page_data
        :param page_id:
        :param data_name:
        :param data_source_type:
        :param data_update_freq:
        :param data_update_time:
        :param data_tabs:
        :param page_data_confs:
        :return:
        """
        key = PageDataDao().insert(page_id, data_name, data_source_type, data_update_freq, data_update_time)
        if key > 0:
            for x in data_tabs:
                self.add_data_tab(x[0], key, x[1], x[2], x[3], x[4])
            if page_data_confs is not None:
                for x in page_data_confs:
                    PageDataConfDao().insert(key, x[0], x[1], x[2], x[3])
        page_data = self.get_page_data(key)
        return page_data

    def delete_page_data(self, page_data_id):
        """
        级联删除page_data、data_tab、page_data_confs、data_tab_columns数据
        :param page_data_id:
        :return:
        """
        page_data = self.get_page_data(page_data_id)
        PageDataConfDao().delete_by_page_data_id(page_data_id)
        PageDataDao().delete(page_data_id)
        for data_tab in page_data.data_tabs:
            DataTabColumnDao().delete_by_data_tab_id(data_tab.id)
            DataTabDao().delete(data_tab.id)
        page_data = self.get_page_data(page_data_id)
        return page_data

    def _get_data_tab_columns(self, tab_id):
        data = DataTabColumnDao().query_by_tab_id(tab_id)
        if data:
            data_tab_columns = []
            for row in data:
                data_tab_columns.append(DataTabColumnEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
            return data_tab_columns
        else:
            Logging.error('不存在该data_tab_id:', tab_id)

    def _get_data_tab(self, tab_id):
        data = DataTabDao().query(tab_id)
        if data:
            data = data[0]
            data_tab_column_entity = self._get_data_tab_columns(tab_id)
            data_tab = DataTabEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data_tab_column_entity)
            return data_tab
        else:
            Logging.error('不存在该tab_id:', tab_id)

    def _get_data_tabs(self, page_data_id):
        data_tabs = []
        data = DataTabDao().query_by_page_data_id(page_data_id)
        if data:
            for row in data:
                data_tab = self._get_data_tab(row[0])
                data_tabs.append(data_tab)
            return data_tabs
        else:
            Logging.error('不存在该page_data_id:', page_data_id)

    def add_data_tab(self, name, page_data_id, check_name_rule, business_columns, pre_cnt, data_tab_columns):
        """
        增加data_table
        :param name:
        :param page_data_id:
        :param check_name_rule:
        :param business_columns:
        :param pre_cnt:
        :param data_tab_columns:
        :return:
        """
        tab_key = DataTabDao().insert(name, page_data_id, check_name_rule, business_columns, pre_cnt)
        if data_tab_columns is not None and tab_key > 0:
            for x in data_tab_columns:
                DataTabColumnDao().insert(tab_key, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
        data_tab = self._get_data_tab(tab_key)
        return data_tab

