from common.db import DB
from handle.common.time import get_current_timestamp


class StoreDao:
    def insert(self, name, plt_name, plt_store_id, login_username=None, url=None, status=1):
        DB.insert("insert into t_store (name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(name, plt_name, plt_store_id, login_username, url, status, get_current_timestamp(), get_current_timestamp()))

    def query_by_id(self, id):
        data = DB.query_fetchall('select id, name, plt_name, plt_store_id, login_username, url, status, created, updated from t_store where id = {}'.format(id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_store where id = {}'.format(id))
        return True


class StorePropertyDao:
    def insert(self, store_id, p_type, p_key, p_value, p_description):
        DB.insert('insert into t_store_property (store_id, p_type, p_key, p_value, p_description, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(store_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))

    def query_by_store_id(self, store_id):
        data = DB.query_fetchall('select id, store_id, p_type, p_key, p_value, p_description, created, updated from t_store_property where store_id = {}'.format(store_id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_store_property where id = {}'.format(id))
