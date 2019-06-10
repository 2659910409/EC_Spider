from common.db import DB


# TODO 补全增加、删除操作
class StoreDAO:
    def __init__(self, store_id):
        self.id = None
        self.store_name = None
        self.plt_name = None
        self.plt_store_id = None
        self.status = None
        self.url = None
        self.created = None
        self.updated = None
        self._init_by_id(store_id)

    def _init_by_id(self, store_id):
        rows = DB.query('select id, store_name, plt_name, plt_store_id, login_username, status, url, created, updated from t_store where store_id = \''+store_id+'\';')
        if len(rows) == 1:
            self.id = rows[0][0]
            self.store_name = rows[0][1]
            self.plt_name = rows[0][2]
            self.plt_store_id = rows[0][3]
            self.status = rows[0][4]
            self.url = rows[0][5]
            self.created = rows[0][6]
            self.updated = rows[0][7]
        else:
            print('未找到store_id对应实例,store_id:', store_id)
            raise Exception


class StorePropertyDAO:
    def __init__(self, store_id):
        self.id = None
        self.store_id = None
        self.p_type = None
        self.p_key = None
        self.p_value = None
        self.p_description = None
        self.created = None
        self.updated = None
        self._init_by_id(store_id)

    def _init_by_id(self, store_id):
        rows = DB.query('select id, store_name from t_store where store_id = \''+store_id+'\';')
        if len(rows) == 1:
            self.id = rows[0][0]
            self.store_id = rows[0][1]
            self.p_type = rows[0][2]
            self.p_key = rows[0][3]
            self.p_value = rows[0][4]
            self.p_description = rows[0][5]
            self.created = rows[0][6]
            self.updated = rows[0][7]
        else:
            print('未找到store_id对应实例,store_id:', store_id)
            raise Exception
