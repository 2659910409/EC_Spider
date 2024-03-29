from common.db import DataBase
from common.util_time import get_current_timestamp


class PageDao:
    def __init__(self):
        self.db = DataBase()

    def insert(self, website, name, menu_level_first, url, menu_level_second=None, menu_level_third=None):
        key = self.db.insert("insert into ec_spider.t_page (website, name, menu_level_first, menu_level_second, menu_level_third, url, created, updated) values(%s{})".format(", %s"*7), (website, name, menu_level_first, menu_level_second, menu_level_third, url, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query(self, id):
        data = self.db.query("select id, website, name, menu_level_first, menu_level_second, menu_level_third, url, created, updated from ec_spider.t_page where id = {}".format(id))
        return data

    def delete(self, id):
        self.db.delete("delete from ec_spider.t_page where id = {}".format(id))
        self.db.commit()


class DataTabColumnDao:
    def __init__(self):
        self.db = DataBase()

    def insert(self, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk):
        key = self.db.insert("insert into ec_spider.t_data_tab_column (data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated) values(%s{})".format(", %s"*10), (data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query_by_tab_id(self, tab_id):
        data = self.db.query("select id, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated from ec_spider.t_data_tab_column where data_tab_id = {}".format(tab_id))
        return data

    def delete(self, id):
        self.db.delete("delete from ec_spider.t_data_tab_column where id = {}".format(id))

    def delete_by_data_tab_id(self, data_tab_id):
        self.db.delete("delete from ec_spider.t_data_tab_column where data_tab_id = {}".format(data_tab_id))
        self.db.commit()


class PageDataConfDao:
    def __init__(self):
        self.db = DataBase()

    def insert(self, page_data_id, p_type, p_key, p_value, p_description):
        key = self.db.insert("insert into ec_spider.t_page_data_conf (page_data_id, p_type, p_key, p_value, p_description, created, updated) values(%s{})".format(", %s"*6), (page_data_id, p_type, p_key, p_value, p_description, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query_by_page_data_id(self, page_data_id):
        data = self.db.query("select id, page_data_id, p_type, p_key, p_value, p_description, created, updated from ec_spider.t_page_data_conf where page_data_id = {}".format(page_data_id))
        return data

    def delete(self, id):
        self.db.delete("delete from ec_spider.t_page_data_conf where id = {}".format(id))

    def delete_by_page_data_id(self, page_data_id):
        self.db.delete("delete from ec_spider.t_page_data_conf where page_data_id = {}".format(page_data_id))
        self.db.commit()


class PageDataDao:
    def __init__(self):
        self.db = DataBase()

    def insert(self, page_id, name, status, data_source_type, data_update_freq, data_update_time, rule_read_file_prefix, rule_save_path_suffix):
        key = self.db.insert("insert into ec_spider.t_page_data (page_id, name, status, data_source_type, data_update_freq, data_update_time, rule_read_file_prefix, rule_save_path_suffix, created, updated) values(%s{})".format(", %s"*9), (page_id, name, status, data_source_type, data_update_freq, data_update_time, rule_read_file_prefix, rule_save_path_suffix, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query(self, id):
        data = self.db.query("select id, page_id, name, status, data_source_type, data_update_freq, data_update_time, rule_read_file_prefix, rule_save_path_suffix, created, updated from ec_spider.t_page_data where id = {}".format(id))
        return data

    def query_by_page_id(self, page_id):
        data = self.db.query("select id, page_id, name, status, data_source_type, data_update_freq, data_update_time, rule_read_file_prefix, rule_save_path_suffix, created, updated from ec_spider.t_page_data where page_id = {}".format(page_id))
        return data

    def delete(self, id):
        self.db.delete("delete from ec_spider.t_page_data where id = {}".format(id))
        self.db.commit()


class DataTabDao:
    def __init__(self):
        self.db = DataBase()

    def insert(self, name, page_data_id, check_name_rule, business_columns, pre_cnt=1):
        key = self.db.insert("insert into ec_spider.t_data_tab (name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated) values(%s{})".format(", %s"*6), (name, page_data_id, check_name_rule, business_columns, pre_cnt, get_current_timestamp(), get_current_timestamp()))
        self.db.commit()
        return key

    def query_by_page_data_id(self, page_data_id):
        data = self.db.query("select id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated from ec_spider.t_data_tab where page_data_id = {}".format(page_data_id))
        return data
    
    def query(self, id):
        data = self.db.query("select id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated from ec_spider.t_data_tab where id = {}".format(id))
        return data
    
    def delete(self, id):
        self.db.delete("delete from ec_spider.t_data_tab where id = {}".format(id))
        self.db.commit()

