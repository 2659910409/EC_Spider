
class Store:
    def __init__(self, **columns):
        # for key, value in columns.items():
        #     self.key = value
        self.id = columns['id']
        self.name = columns['name']
        self.plt_name = columns['plt_name']
        self.plt_store_id = columns['plt_store_id']
        self.login_username = columns['login_username']
        self.status = columns['status']
        self.url = columns['url']
        self.created = columns['created']
        self.updated = columns['updated']


class StoreProperty:
    def __init__(self, columns):
        self.id = columns['id']
        self.store_id = columns['store_id']
        self.p_type = columns['p_type']
        self.p_key = columns['p_key']
        self.p_value = columns['p_value']
        self.p_description = columns['p_decription']
        self.created = columns['created']
        self.updated = columns['updated']