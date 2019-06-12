from dao.page_data_dao import *
from entity.page_data import *


class PageService:
    def get_page(self, page_id):
        data = PageDao().query_by_id(page_id)
        if data:
            id = data[0]
            website = data[1]
            menulevel_first = data[2]
            menulevel_second = data[3]
            menulevel_third = data[4]
            url = data[5]
            created = data[6]
            updated = data[7]
            page = PageEntity(id, website, menulevel_first, menulevel_second, menulevel_third, url, created, updated)
            return page
        else:
            print('页面id不存在:', page_id)

    def get_pages(self, page_ids):
        pages = []
        for page_id in page_ids:
            _page = self.get_page(page_id)
            if _page is not None:
                pages.append(_page)
        return pages


class PageDataService:
    def get_page_data(self, page_data_id):
        data = PageDataDao().query_by_id(page_data_id)
        if data:
            id = data[0]
            page_id = data[1]
            data_name = data[2]
            data_source_type = data[3]
            data_update_freq = data[4]
            data_update_time = data[5]
            created = data[6]
            updated = data[7]
            page_data = PageDataEntity(id, page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated)
            return page_data
        else:
            print('不存在该page_data_id:', page_data_id)

    def get_page_datas(self, page_data_ids):
        page_datas = []
        for page_data_id in page_data_ids:
            _page_data = self.get_page_data(page_data_id)
            if _page_data is not None:
                page_datas.append(_page_data)
        return page_datas

    def get_page_data_columns(self, tab_id):
        data = PageDataColumnDao().query_by_tab_id(tab_id)
        if data:
            page_data_columns = []
            for row in data:
                id = row[0]
                data_tab_id = row[1]
                col_name = row[2]
                col_type = row[3]
                col_type_length = row[4]
                col_description = row[5]
                check_col_name = row[6]
                is_file_column = row[7]
                is_primary_key = row[8]
                is_data_maintenance_pk = row[9]
                created = row[10]
                updated = row[11]
                page_data_columns.append(PageDataColumnEntity(id, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated))
            return page_data_columns
        else:
            print('不存在该data_tab_id:', tab_id)

    def get_page_data_confs(self, page_data_id):
        data = PageDataConfDao().query_by_page_data_id(page_data_id)
        if data:
            page_data_confs = []
            for row in data:
                id = row[0]
                page_data_id = row[1]
                p_type = row[2]
                p_key = row[3]
                p_value = row[4]
                p_description = row[5]
                created = row[10]
                updated = row[11]
                page_data_confs.append(
                    PageDataConfEntity(id, page_data_id, p_type, p_key, p_value, p_description, created,
                                       updated))
            return page_data_confs
        else:
            print('不存在该page_data_id:', page_data_id)

    def get_data_tabs(self, page_data_id):
        data = DataTabDao().query_by_page_data_id(page_data_id)
        if data:
            data_tabs = []
            for row in data:
                id = row[0]
                name = row[1]
                page_data_id = row[2]
                check_name_rule = row[3]
                business_columns = row[4]
                pre_cnt = row[5]
                created = row[6]
                updated = row[7]
                data_tabs.append(DataTabEntity(id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated))
            return data_tabs
        else:
            print('不存在该page_data_id:', page_data_id)

    # def get_columns(self, page_data):
    #     columns = []
    #     for x in page_data.page_data_columns:
    #         columns.append(x.col_name)
    #     return columns
    #
    # def get_file_columns(self, page_data):
    #     columns = []
    #     for x in page_data.page_data_columns:
    #         if x.is_file_column == 1:
    #             columns.append(x.col_name)
    #     return columns
    #
    # def set_file_column_flag(self, page_data, columns):
    #     """
    #     文件title 与 配置表所需字段匹配，匹配到为存在，设置is_exists_file = True
    #     :param columns: file title列表
    #     :return: True
    #     """
    #     for f_col_name in columns:
    #         for t_col in page_data.page_data_columns:
    #             if t_col.check_col_name == f_col_name:
    #                 t_col.is_exists_file = True
    #     return page_data
    #
    # def get_file_exists_columns(self, page_data):
    #     columns = []
    #     for t_col in self.page_data.page_data_columns:
    #         if t_col.is_exists_file == 1:
    #             columns.append(t_col.col_name)
    #     return columns

