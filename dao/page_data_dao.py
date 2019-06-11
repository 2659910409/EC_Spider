from common.db import DB
from common.logging import Logging


class PageDao:
    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.col_names = self._get_columns()
        self.col_cnt = len(self.col_names)

    def _get_columns(self):
        """
        获取表的字段名
        :return:
        """
        columns_name = []
        rows = DB.query_fetchall("select column_name from information_schema.columns where table_name = {};".format(self.tab_name))
        for row in rows:
            columns_name.append(row)
        return columns_name


    def insert(self, name, plt_name, plt_store_id, properties, login_username=None, url=None):
        DB.insert("insert into t_store(name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, 1, now(), now())".format(name, plt_name, plt_store_id, login_username, url))

    def query_by_store_id(self, store_id):
        row = DB.query_fetchall('select {} from {} where plt_store_id = {}'.format(','.join(self.col_names), self.tab_name, store_id))
        store_info = dict(self.col_names, list(row))
        store = Store(store_info)
        return store

    def delete_by_store_id(self, store_id):
        DB.detele('delete from {} where id = {}'.format(self.tab_name, store_id))


class PageDataColumnDao:
    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.col_names = self._get_columns()
        self.col_cnt = len(self.col_names)

    def _get_columns(self):
        """
        获取表的字段名
        :return:
        """
        columns_name = []
        rows = DB.query_fetchall("select column_name from information_schema.columns where table_name = {};".format(self.tab_name))
        for row in rows:
            columns_name.append(row)
        return columns_name


    def insert(self, name, plt_name, plt_store_id, properties, login_username=None, url=None):
        DB.insert("insert into t_store(name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, 1, now(), now())".format(name, plt_name, plt_store_id, login_username, url))

    def query_by_store_id(self, store_id):
        row = DB.query_fetchall('select {} from {} where plt_store_id = {}'.format(','.join(self.col_names), self.tab_name, store_id))
        store_info = dict(self.col_names, list(row))
        store = Store(store_info)
        return store

    def delete_by_store_id(self, store_id):
        DB.detele('delete from {} where id = {}'.format(self.tab_name, store_id))


class PageDataConfDao:
    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.col_names = self._get_columns()
        self.col_cnt = len(self.col_names)

    def _get_columns(self):
        """
        获取表的字段名
        :return:
        """
        columns_name = []
        rows = DB.query_fetchall("select column_name from information_schema.columns where table_name = {};".format(self.tab_name))
        for row in rows:
            columns_name.append(row)
        return columns_name


    def insert(self, name, plt_name, plt_store_id, properties, login_username=None, url=None):
        DB.insert("insert into t_store(name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, 1, now(), now())".format(name, plt_name, plt_store_id, login_username, url))

    def query_by_store_id(self, store_id):
        row = DB.query_fetchall('select {} from {} where plt_store_id = {}'.format(','.join(self.col_names), self.tab_name, store_id))
        store_info = dict(self.col_names, list(row))
        store = Store(store_info)
        return store

    def delete_by_store_id(self, store_id):
        DB.detele('delete from {} where id = {}'.format(self.tab_name, store_id))


class PageDataDao:
    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.col_names = self._get_columns()
        self.col_cnt = len(self.col_names)

    def _get_columns(self):
        """
        获取表的字段名
        :return:
        """
        columns_name = []
        rows = DB.query_fetchall("select column_name from information_schema.columns where table_name = {};".format(self.tab_name))
        for row in rows:
            columns_name.append(row)
        return columns_name


    def insert(self, name, plt_name, plt_store_id, properties, login_username=None, url=None):
        DB.insert("insert into t_store(name, plt_name, plt_store_id, login_username, url, status, created, updated) values({1}, {2}, {3}, {4}, {5}, 1, now(), now())".format(name, plt_name, plt_store_id, login_username, url))

    def query_by_store_id(self, store_id):
        row = DB.query_fetchall('select {} from {} where plt_store_id = {}'.format(','.join(self.col_names), self.tab_name, store_id))
        store_info = dict(self.col_names, list(row))
        store = Store(store_info)
        return store

    def delete_by_store_id(self, store_id):
        DB.detele('delete from {} where id = {}'.format(self.tab_name, store_id))

