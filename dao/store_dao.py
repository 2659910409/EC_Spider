from common.db import DB


# TODO 补全增加、删除操作
class StoreDAO:
    def __init__(self):
        self.id = None
        self.store_name = None
        self.plt_name = None
        self.plt_store_id = None
        self.status = None
        self.url = None
        self.created = None
        self.updated = None
        self.store_properties = []


class StorePropertyDAO:
    def __init__(self):
        self.id = None
        self.store_id = None
        self.p_type = None
        self.p_key = None
        self.p_value = None
        self.p_description = None
        self.created = None
        self.updated = None
