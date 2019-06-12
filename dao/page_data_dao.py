from common.db import DB
from common.logging import Logging
from handle.common.time import get_current_timestamp
from entity.page_data import *


class PageDao:
    def insert(self, website, menulevel_first, url, menulevel_second=None, menulevel_third=None):
        DB.insert("insert into t_page (website, menulevel_first, menulevel_second, menulevel_third, url, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(website, menulevel_first, menulevel_second, menulevel_third, url, get_current_timestamp(), get_current_timestamp()))

    def query_by_id(self, id):
        data = DB.query_fetchall('select id, website, menulevel_first, menulevel_second, menulevel_third, url, created, updated from t_page where id = {}'.format(id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_page where id = {}'.format(id))


class PageDataColumnDao:
    def insert(self, data_tab_id, col_name, col_type, check_col_name, is_primary_key, is_data_maintenance_pk, is_file_column=None,col_type_length=None, col_description=None):
        DB.insert("insert into t_page_data_column (data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})".format(data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, get_current_timestamp(), get_current_timestamp()))

    def query_by_tab_id(self, tab_id):
        data = DB.query_fetchall('select id, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated from t_page_data_column where id = {}'.format(tab_id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_page_data_column where id = {}'.format(id))

    def delete_by_data_tab_id(self, data_tab_id):
        DB.detele('delete from t_page_data_column where data_tab_id = {}'.format(data_tab_id))


class PageDataConfDao:
    def insert(self, page_data_id, p_type, p_key, p_value, p_description):
        DB.insert("insert into t_page_data_conf (page_data_id, p_type, p_key, p_value, p_description, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(page_data_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))

    def query_by_page_data_id(self, page_data_id):
        data = DB.query_fetchall('select id, page_data_id, p_type, p_key, p_value, p_description, created, updated from t_page_data where page_data_id = {}'.format(page_data_id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_page_data_conf where id = {}'.format(id))

    def delete_by_page_data_id(self, page_data_id):
        DB.detele('delete from t_page_data_conf where page_data_id = {}'.format(page_data_id))


class PageDataDao:
    def insert(self, page_id, data_name, data_source_type, data_update_freq, data_update_time):
        DB.insert("insert into t_page (page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(page_id, data_name, data_source_type, data_update_freq, data_update_time, get_current_timestamp(), get_current_timestamp()))

    def query_by_id(self, id):
        data = DB.query_fetchall('select id, page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated from t_page_data where id = {}'.format(id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_page_data where id = {}'.format(id))


class DataTabDao:
    def insert(self, name, page_data_id, check_name_rule, business_columns, pre_cnt=1):
        DB.insert("insert into t_data_tab (name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(name, page_data_id, check_name_rule, business_columns, pre_cnt, get_current_timestamp(), get_current_timestamp()))

    def query_by_page_data_id(self, page_data_id):
        data = DB.query_fetchall('select id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated from t_data_tab where page_data_id = {}'.format(page_data_id))
        return data

    def delete_by_id(self, id):
        DB.detele('delete from t_data_tab where id = {}'.format(id))

