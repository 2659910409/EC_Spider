from common.db import DB
from handle.common.time import get_current_timestamp


class StoreDao:
    def __init__(self):
        self.self.db = DB()
        
    def insert(self, name, plt_name, plt_store_id, login_username=None, url=None, status=1):
        key = self.db.insert("insert into t_store (name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(name, plt_name, plt_store_id, login_username, url, status, get_current_timestamp(), get_current_timestamp()))
        return key

    def query(self, id):
        data = self.db.query_fetchall('select id, name, plt_name, plt_store_id, login_username, url, status, created, updated from t_store where id = {}'.format(id))
        return data

    def query_by_name(self, name):
        data = self.db.query_fetchall('select id, name, plt_name, plt_store_id, login_username, url, status, created, updated from t_store where name = {}'.format(name))
        return data

    def delete(self, id):
        self.db.detele('delete from t_store where id = {}'.format(id))
        return True


class StorePropertyDao:
    def insert(self, store_id, p_type, p_key, p_value, p_description):
        key = self.db.insert('insert into t_store_property (store_id, p_type, p_key, p_value, p_description, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(store_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))
        return key

    def query_by_store_id(self, store_id):
        data = self.db.query_fetchall('select id, store_id, p_type, p_key, p_value, p_description, created, updated from t_store_property where store_id = {}'.format(store_id))
        return data

    def delete(self, id):
        self.db.detele('delete from t_store_property where id = {}'.format(id))
