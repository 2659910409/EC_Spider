from common.db import DB
from common.logging import Logging
from handle.common.time import get_current_timestamp
from entity.page_data import *


class PageDao:
    def insert(self, website, menulevel_first, url, menulevel_second=None, menulevel_third=None):
        DB.insert("insert into t_page (website, menulevel_first, menulevel_second, menulevel_third, url, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(website, menulevel_first, menulevel_second, menulevel_third, url, get_current_timestamp(), get_current_timestamp()))

    def query_by_page_id(self, page_id):
        row = DB.query_fetchall('select id, website, menulevel_first, menulevel_second, menulevel_third, url, created, updated from t_page where id = {}'.format(page_id))
        id = row[0]
        website = row[1]
        menulevel_first = row[2]
        menulevel_second = row[3]
        menulevel_third = row[4]
        url = row[5]
        created = row[6]
        updated = row[7]
        page = PageEntity(id, website, menulevel_first, menulevel_second, menulevel_third, url, created, updated)
        return page

    def delete_by_id(self, id):
        DB.detele('delete from t_page where id = {}'.format(id))


class PageDataColumnDao:
    def insert(self, data_tab_id, col_name, col_type, check_col_name, is_primary_key, is_data_maintenance_pk, is_file_column=None,col_type_length=None, col_description=None):
        DB.insert("insert into t_page_data_column (data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})".format(data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, get_current_timestamp(), get_current_timestamp()))

    def query_by_tab_id(self, tab_id):
        page_data_columns = []
        rows = DB.query_fetchall('select id, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated from t_page_data_column where id = {}'.format(tab_id))
        for row in rows:
            id = row[0]
            data_tab_id = row[1]
            col_name = row[2]
            col_type = row[3]
            col_type_length = row[4]
            col_description = row[5]
            check_col_name = row[6]
            is_file_column = row[7]
            is_primary_key = row[8]
            is_data_maintenance_pk = row[9]
            created = row[10]
            updated = row[11]
            page_data_columns.append(PageDataColumnEntity(id, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated))
        return page_data_columns

    def delete_by_id(self, id):
        DB.detele('delete from t_page_data_column where id = {}'.format(id))

    def delete_by_data_tab_id(self, data_tab_id):
        DB.detele('delete from t_page_data_column where data_tab_id = {}'.format(data_tab_id))


class PageDataConfDao:
    def insert(self, page_data_id, p_type, p_key, p_value, p_description):
        DB.insert("insert into t_page_data_conf (page_data_id, p_type, p_key, p_value, p_description, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(page_data_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))

    def query_by_page_data_id(self, page_data_id):
        page_data_confs = []
        rows = DB.query_fetchall('select id, page_data_id, p_type, p_key, p_value, p_description, created, updated from t_page_data where page_data_id = {}'.format(page_data_id))
        for row in rows:
            id = row[0]
            page_data_id = row[1]
            p_type = row[2]
            p_key = row[3]
            p_value = row[4]
            p_description = row[5]
            created = row[10]
            updated = row[11]
            page_data_confs.append(PageDataConfEntity(id, page_data_id, p_type, p_key, p_value, p_description, created, updated))
        return page_data_confs

    def delete_by_id(self, id):
        DB.detele('delete from t_page_data_conf where id = {}'.format(id))

    def delete_by_page_data_id(self, page_data_id):
        DB.detele('delete from t_page_data_conf where page_data_id = {}'.format(page_data_id))


class PageDataDao:
    def insert(self, page_id, data_name, data_source_type, data_update_freq, data_update_time):
        DB.insert("insert into t_page (page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(page_id, data_name, data_source_type, data_update_freq, data_update_time, get_current_timestamp(), get_current_timestamp()))

    def query_by_id(self, id):
        row = DB.query_fetchall('select id, page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated from t_page_data where id = {}'.format(id))
        id = row[0]
        page_id = row[1]
        data_name = row[2]
        data_source_type = row[3]
        data_update_freq = row[4]
        data_update_time = row[5]
        created = row[6]
        updated = row[7]
        page_data = PageDataEntity(id, page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated)
        return page_data

    def delete_by_id(self, id):
        DB.detele('delete from t_page_data where id = {}'.format(id))


class DataTabDao:
    def insert(self, name, page_data_id, check_name_rule, business_columns, pre_cnt=1):
        DB.insert("insert into t_data_tab (name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated) values({1}, {2}, {3}, {4}, {5}, {6}, {7})".format(name, page_data_id, check_name_rule, business_columns, pre_cnt, get_current_timestamp(), get_current_timestamp()))

    def query_by_page_data_id(self, page_data_id):
        data_tabs = []
        rows = DB.query_fetchall('select id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated from t_data_tab where page_data_id = {}'.format(page_data_id))
        for row in rows:
            id = row[0]
            name = row[1]
            page_data_id = row[2]
            check_name_rule = row[3]
            business_columns = row[4]
            pre_cnt = row[5]
            created = row[6]
            updated = row[7]
            data_tabs.append(DataTabEntity(id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated))
        return data_tabs

    def delete_by_id(self, id):
        DB.detele('delete from t_data_tab where id = {}'.format(id))

