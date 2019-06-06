from common.db import DB


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
        rows = DB.query('select id, store_name from t_store where store_id = \''+store_id+'\';')
        if len(rows) == 1:
            self.id = rows[0][0]
            self.store_name = rows[0][1]

    def _init_by_name(self, store_name):
        pass

    def save(self, store_name):
        _id = DB.insert('insert into t_store(store_name) values(\'+store_name+\');')
        if _id is not None:
            self.id = _id
            self.store_name = store_name
