from common.db import DataBase
from common.util_time import get_current_timestamp


class StoreDao:
    def __init__(self):
        self.db = DataBase()
        
    def insert(self, name, plt_name, plt_store_id, login_username=None, url=None, status=1):
        key = self.db.insert("insert into ec_spider.t_store (name, plt_name, plt_store_id, login_username, url, status, created, updated) values(%s{})".format(', %s'*7), (name, plt_name, plt_store_id, login_username, url, status, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query(self, id):
        data = self.db.query("select id, name, plt_name, plt_store_id, login_username, url, status, created, updated from ec_spider.t_store where id = {}".format(id))
        return data

    def query_by_name(self, store_name):
        data = self.db.query("select id, name, plt_name, plt_store_id, login_username, url, status, created, updated from ec_spider.t_store where name = '{}'".format(store_name))
        return data

    def delete(self, id):
        self.db.delete("delete from ec_spider.t_store where id = {}".format(id))
        self.db.commit()
        return True


class StorePropertyDao:
    def __init__(self):
        self.db = DataBase()

    def insert(self, store_id, p_type, p_key, p_value, p_description):
        key = self.db.insert("insert into ec_spider.t_store_property (store_id, p_type, p_key, p_value, p_description, created, updated) values(%s{})".format(', %s'*6), (store_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query_by_store_id(self, store_id):
        data = self.db.query("select id, store_id, p_type, p_key, p_value, p_description, created, updated from ec_spider.t_store_property where store_id = {}".format(store_id))
        return data

    def delete(self, id):
        self.db.delete("delete from ec_spider.t_store_property where id = {}".format(id))
        self.db.commit()

    def delete_by_store_id(self, store_id):
        self.db.delete("delete from ec_spider.t_store_property where store_id = {}".format(store_id))
        self.db.commit()

