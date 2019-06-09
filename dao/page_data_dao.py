from common.db import DB


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
            print('未找到page_id 对应实例，page_id:', page_id)
            raise Exception

class PageDataColumnDao:
    def __init__(self):
        pass

class PageDataDao:
    def __init__(self, page_data_id):
        self.id = None
        self.page_id = None
        self.page = None
        # TODO 待完善
        self.created = None
        self.updated = None
        self.PageDataColumns = []
        self._init_by_id(page_data_id)

    def _init_by_id(self, page_data_id):
        rows = DB.query('select id, page_id, data_name from t_page_data where page_data_id = \''+page_data_id+'\';')
        if len(rows) == 1:
            self.id = rows[0][0]
            self.store_name = rows[0][1]
        self.page = PageDao(self.page_id)
        rows = DB.query('select p_type, p_key, p_value, p_description from t_page_data_conf where page_data_id = \''+page_data_id+'\';')
        # TODO pageDao 完善
        # TODO pageDataColumn 完善

    def _init_by_name(self, store_name):
        pass
