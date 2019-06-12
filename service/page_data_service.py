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


class PageDataService:
    def get_page_data(self, page_data_id):
        """
        获取页面数据块信息
        :param page_data_id: 页面数据块id
        :return: 页面数据块的实体对象
        """
        data = PageDataDao().query_by_id(page_data_id)
        if data:
            page_data_conf_entity = self.get_page_data_confs(page_data_id)
            page_data = PageDataEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], page_data_conf_entity)
            return page_data
        else:
            print('不存在该page_data_id:', page_data_id)

    def get_page_datas_by_page(self, page_id):
        data = PageDataDao.query_by_page_id(page_id)
        if data:
            page_data_ids = []
            page_datas = []
            for row in data:
                page_data_ids.append(page_data_ids)
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
                page_data_confs.append(PageDataConfEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
            return page_data_confs
        else:
            print('不存在该page_data_id:', page_data_id)


class DataTabService:
    def get_page_data_columns(self, tab_id):
        data = PageDataColumnDao().query_by_tab_id(tab_id)
        if data:
            page_data_columns = []
            for row in data:
                page_data_columns.append(PageDataColumnEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))
            return page_data_columns
        else:
            print('不存在该data_tab_id:', tab_id)

    def get_data_tab(self, tab_id):
        data = DataTabDao.query(tab_id)
        if data:
            page_data_column_entity = self.get_page_data_columns(tab_id)
            data_tab = DataTabEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], page_data_column_entity)
            return data_tab
        else:
            print('不存在该tab_id:', tab_id)


