from common.db import DB
from common.logging import Logging


class PageDao:
    def __init__(self, page_id):
        self.id = page_id
        self.website = None
        self.mean_level_first = None
        self.mean_level_two = None
        self.mean_level_third = None
        self.url = None
        self.created = None
        self.updated = None
        self._init_by_id(page_id)

    def _init_by_id(self, page_id):
        rows = DB.query('select id, website, mean_level_first, mean_level_two, mean_level_third, url, created, updated  from t_page where id = '+page_id+';')
        if len(rows) == 1:
            self.website = rows[0][1]
            self.mean_level_first = rows[0][2]
            self.mean_level_two = rows[0][3]
            self.mean_level_third = rows[0][4]
            self.url = rows[0][5]
            self.created = rows[0][6]
            self.updated = rows[0][7]
        else:
            Logging.error('未找到page_id 对应实例，page_id:' + page_id)
            raise Exception


class PageDataColumnDao:
    def __init__(self, row):
        self.id = row[0]
        self.page_data_id = row[1]
        self.col_name = row[2]
        self.col_type = row[3]
        self.col_description = row[4]
        self.check_col_name = row[5]
        self.col_name = row[6]
        self.is_file_column = row[7]
        self.is_primary_key = row[8]
        self.is_data_maintenance = row[9]
        self.created = row[10]
        self.updated = row[11]
        self.is_exists_file = False


class PageDataConfDao:
    def __init__(self, page_data_conf_id):
        self.id = page_data_conf_id
        self.page_data_id = None
        self.p_type = None
        self.p_key = None
        self.p_value = None
        self.p_description = None
        self.created = None
        self.updated = None
        self._init_by_id(page_data_conf_id)

    def _init_by_id(self, page_data_conf_id):
        rows = DB.query('select id, page_data_id, p_type, p_key, p_value, p_description, created, updated from t_page_data_conf where page_data_conf_id = \''+page_data_conf_id+'\';')
        if len(rows) == 1:
            self.page_id = rows[0][1]
            self.data_name = rows[0][2]
            self.table_name = rows[0][3]
            self.data_business_columns = rows[0][4]
            self.data_pre_cnt = rows[0][5]
            self.data_source_type = rows[0][6]
            self.data_update_freq = rows[0][7]
            self.data_update_time = rows[0][8]
            self.created = rows[0][9]
            self.updated = rows[0][10]
        else:
            print('page_data_conf_id对应实例,page_data_conf_id:', page_data_conf_id)
            raise Exception


class PageDataDao:
    def __init__(self, page_data_id):
        self.id = page_data_id
        self.page_id = None
        self.data_name = None
        self.table_name = None
        self.data_business_columns = None
        self.data_pre_cnt = None
        self.data_source_type = None
        self.data_update_freq = None
        self.data_update_time = None
        self.created = None
        self.updated = None
        self.page = None
        self.page_data_columns = []
        self.page_data_confs = []
        self._init_by_id(page_data_id)

    def _init_by_id(self, page_data_id):
        rows = DB.query('select id, page_id, data_name, table_name, data_business_columns, data_pre_cnt, data_source_type, data_update_freq, data_update_time, created, updated from t_page_data where page_data_id = \''+page_data_id+'\';')
        if len(rows) == 1:
            self.page_id = rows[0][1]
            self.data_name = rows[0][2]
            self.table_name = rows[0][3]
            self.data_business_columns = rows[0][4]
            self.data_pre_cnt = rows[0][5]
            self.data_source_type = rows[0][6]
            self.data_update_freq = rows[0][7]
            self.data_update_time = rows[0][8]
            self.created = rows[0][9]
            self.updated = rows[0][10]
        else:
            Logging.error('未找到page_data_id 对应实例,page_data_id:' + page_data_id)
            raise Exception
        self.page = PageDao(self.page_id)
        rows = DB.query('select id, page_data_id, col_name, col_type, col_description, check_col_name, col_name, is_file_column, is_primary_key, is_data_maintenance, created, updated  from t_page_data_column where id = ' + page_data_id + ';')
        for row in rows:
            self.page_data_columns.append(PageDataColumnDao(row))
        rows = DB.query('select id, p_type, p_key, p_value, p_description from t_page_data_conf where page_data_id = \''+page_data_id+'\';')
        for row in rows:
            self.page_data_confs.append(PageDataConfDao(row))
