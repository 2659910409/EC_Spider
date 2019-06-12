from common.db import DB
from dao.store_dao import StoreDao, StorePropertyDao
from entity.store import StoreEntity, StorePropertyEntity


class StoreService:
    def get_store(self, store_id):
        data = StoreDao().query_by_id(store_id)
        if data:
            id = data[0]
            name = data[1]
            plt_name = data[2]
            plt_store_id = data[3]
            login_username = data[4]
            url = data[5]
            status = data[6]
            created = data[7]
            updated = data[8]
            store = StoreEntity(id, name, plt_name, plt_store_id, login_username, url, status, created, updated)
            return store
        else:
            print('店铺id不存在:', store_id)

    def get_stores(self, store_ids):
        stores = []
        for store_id in store_ids:
            _store = self.get_store(store_id)
            if _store:
                stores.append(_store)
        return stores

    def get_store_properties(self, store_id):
        data = StorePropertyDao().query_by_store_id(store_id)
        if data:
            store_properties = []
            for row in data:
                id = row[0]
                store_id = row[1]
                p_type = row[2]
                p_key = row[3]
                p_value = row[4]
                p_description = row[5]
                created = row[6]
                updated = row[7]
                store_properties.append(StorePropertyEntity(id, store_id, p_type, p_key, p_value, p_description, created, updated))
            return store_properties
        else:
            print('该店铺id不存在:', store_id)

    def delete_store_by_id(self, store_id):
        symbol = StoreDao().delete_by_id(store_id)
        return symbol

    def insert(self, name, plt_name, plt_store_id, login_username=None, url=None):
        # if name is None:
        #     raise Exception
        # if self.check_store_name_exists(name):
        #     raise Exception
        # store_id = DB.insert('insert into t_store(name, plt_name, plt_store_id, login_username, url, status, created, updated) values(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 1, now(), now())'.format(name, plt_name, plt_store_id, login_username, url))
        # for property in properties:
        #     store_id = DB.insert('insert into t_store_property(store_id, p_type, p_key_ p_value, p_description, created, updated) values(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', now(), now())'.format(store_id, property.p_type, property.p_key, property.p_value, property.p_description))
        # return self.get_store(store_id)
        pass



