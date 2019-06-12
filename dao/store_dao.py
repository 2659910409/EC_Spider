from common.db import DB
from entity.store import StoreEntity, StorePropertyEntity
from handle.common.time import get_current_timestamp


class StoreDao:
    def insert(self, name, plt_name, plt_store_id, login_username=None, url=None, status=1):
        DB.insert("insert into t_store (name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(name, plt_name, plt_store_id, login_username, url, status, get_current_timestamp(), get_current_timestamp()))

    def query_by_id(self, id):
        row = DB.query_fetchall('select id, name, plt_name, plt_store_id, login_username, url, status, created, updated from t_store where id = {}'.format(id))
        id = row[0]
        name = row[1]
        plt_name = row[2]
        plt_store_id = row[3]
        login_username = row[4]
        url = row[5]
        status = row[6]
        created = row[7]
        updated = row[8]
        store = StoreEntity(id, name, plt_name, plt_store_id, login_username, url, status, created, updated)
        return store

    def delete_by_id(self, id):
        DB.detele('delete from t_store where id = {}'.format(id))


class StoreProperty:
    def insert(self, store_id, p_type, p_key, p_value, p_description):
        DB.insert('insert into t_store_property (store_id, p_type, p_key, p_value, p_description, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(store_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))

    def query_by_store_id(self, store_id):
        store_propertys = []
        rows = DB.query_fetchall('select id, store_id, p_type, p_key, p_value, p_description, created, updated from t_store_property where store_id = {}'.format(store_id))
        for row in rows:
            id = row[0]
            store_id = row[1]
            p_type = row[2]
            p_key = row[3]
            p_value = row[4]
            p_description = row[5]
            created = row[6]
            updated = row[7]
            store_propertys.append(StorePropertyEntity(id, store_id, p_type, p_key, p_value, p_description, created, updated))
        return store_propertys

    def delete_by_id(self, id):
        DB.detele('delete from t_store_property where id = {}'.format(id))
