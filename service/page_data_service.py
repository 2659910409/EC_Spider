from dao.page_data_dao import *
from entity.page_data import *


class PageService:
    def get_page(self, page_id):
        """
        获取需要抓取的页面信息
        :param page_id: 页面id
        :return: page实体对象
        """
        data = PageDao().query_by_id(page_id)
        if data:
            page = PageEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            return page
        else:
            print('页面id不存在:', page_id)

    def add_page(self, website, menu_level_first, url, menu_level_second=None, menu_level_third=None):
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
        if key > 0:
            return True


class PageDataService:
    def get_page_info(self, page_data_id):
        """
        获取页面数据块信息
        :param page_data_id: 页面数据块id
        :return: 页面数据块的实体对象
        """
        data = PageDataDao().query_by_id(page_data_id)
        if data:
            page = PageService().get_page(data[1])
            page_data_conf_entity = self.get_page_data_confs(page_data_id)
            page_data = PageDataEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], page_data_conf_entity)
            return page_data, page
        else:
            print('不存在该page_data_id:', page_data_id)

    def get_page_datas_by_page(self, page_id):
        data = PageDataDao.query_by_page_id(page_id)
        if data:
            page_data_ids = []
            page_datas = []
            for row in data:
                page_data_ids.append(row)
            for page_data_id in page_data_ids:
                _page_data = self.get_page_data(page_data_id)
                if _page_data is not None:
                    page_datas.append(_page_data)
            return page_datas
        else:
            print('不存在该page_id:', page_id)

    def get_page_data_confs(self, page_data_id):
        data = PageDataConfDao().query_by_page_data_id(page_data_id)
        if data:
            page_data_confs = []
            for row in data:
                page_data_confs.append(PageDataConfEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            return page_data_confs
        else:
            print('不存在该page_data_id:', page_data_id)

    def add_page_data(self, page_id, data_name, data_source_type, data_update_freq, data_update_time, page_data_confs=None):
        """
        增加page_data
        :param page_id:
        :param data_name:
        :param data_source_type:
        :param data_update_freq:
        :param data_update_time:
        :param page_data_confs:
        :return:
        """
        key = PageDataDao().insert(page_id, data_name, data_source_type, data_update_freq, data_update_time)
        if page_data_confs is not None and key > 0:
            for x in page_data_confs:
                PageDataConfDao().insert(key, x[0], x[1], x[2], x[3])
        return True


class DataTabService:
    def get_data_tab_columns(self, tab_id):
        data = DataTabColumnDao().query_by_tab_id(tab_id)
        if data:
            data_tab_columns = []
            for row in data:
                data_tab_columns.append(DataTabColumnEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
            return data_tab_columns
        else:
            print('不存在该data_tab_id:', tab_id)

    def get_data_tab(self, tab_id):
        data = DataTabDao.query(tab_id)
        if data:
            data_tab_column_entity = self.get_data_tab_columns(tab_id)
            data_tab = DataTabEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data_tab_column_entity)
            return data_tab
        else:
            print('不存在该tab_id:', tab_id)

    def add_data_tab(self, name, page_data_id, check_name_rule, business_columns, pre_cnt=1, data_tab_columns=None):
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
        return True

    def reduce_data_tab(self, tab_id):
        """
        删除data_tab
        :param tab_id:
        :return:
        """
        DataTabColumnDao().delete_by_data_tab_id(tab_id)
        DataTabDao().delete(tab_id)


    def reduce_page_data(self, page_data_id):
        """删除page_data"""
        PageDataConfDao().delete_by_page_data_id(page_data_id)
        PageDataDao(page_data_id)

