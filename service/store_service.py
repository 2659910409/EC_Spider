from common.db import DB
from dao.store_dao import StoreDAO
from dao.store_dao import StorePropertyDAO


class StoreService:
    def get_store(self, store_id):
        store = StoreDAO()
        rows = DB.query('select id, name, plt_name, plt_store_id, login_username, status, url, created, updated from t_store where store_id = {}'.format(store_id))
        if len(rows) == 1:
            store.id = rows[0][0]
            store.name = rows[0][1]
            store.plt_name = rows[0][2]
            store.plt_store_id = rows[0][3]
            store.status = rows[0][4]
            store.url = rows[0][5]
            store.created = rows[0][6]
            store.updated = rows[0][7]
        else:
            print('未找到store_id对应实例,store_id:', store_id)
            raise Exception
        rows = DB.query('select id, store_name from t_store where store_id = '+store_id+';')
        for row in rows:
            property = StorePropertyDAO()
            property.id = row[0]
            property.store_id = row[1]
            property.p_type = row[2]
            property.p_key = row[3]
            property.p_value = row[4]
            property.p_description = row[5]
            property.created = row[6]
            property.updated = row[7]
            store.store_properties.append(property)
        return store

    def get_stores(self, store_ids):
        stores = []
        for store_id in store_ids:
            _store = self.get_store(store_id)
            if _store is not None:
                stores.append(_store)
        return stores

    def delete_store_by_id(self, store_id):
        DB.delete('delete from t_store where id = {}'.format(store_id))
        return True

    def insert(self, name, plt_name, plt_store_id, properties, login_username=None, url=None):
        if name is None:
            raise Exception
        if self.check_store_name_exists(name):
            raise Exception
        store_id = DB.insert('insert into t_store(name, plt_name, plt_store_id, login_username, url, status, created, updated) values(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 1, now(), now())'.format(name, plt_name, plt_store_id, login_username, url))
        for property in properties:
            store_id = DB.insert('insert into t_store_property(store_id, p_type, p_key_ p_value, p_description, created, updated) values(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', now(), now())'.format(store_id, property.p_type, property.p_key, property.p_value, property.p_description))
        return self.get_store(store_id)

    def check_store_name_exists(self, store_name):
        rows = DB.query('select id, name from t_store where name = \'{}\''.format(store_name))
        if len(rows) > 0:
            return False
        return True
