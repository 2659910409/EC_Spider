
class StoreEntity:
    def __init__(self, id, name, plt_name, plt_store_id, login_username, url, status, created, updated):
        self.id = id
        self.name = name
        self.plt_name = plt_name
        self.plt_store_id = plt_store_id
        self.login_username = login_username
        self.status = status
        self.url = url
        self.created = created
        self.updated = updated


class StorePropertyEntity:
    def __init__(self, id, store_id, p_type, p_key, p_value, p_description, created, updated):
        self.id = id
        self.store_id = store_id
        self.p_type = p_type
        self.p_key = p_key
        self.p_value = p_value
        self.p_description = p_description
        self.created = created
        self.updated = updated