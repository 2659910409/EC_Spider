
class PageEntity:
    def __init__(self, id, website, menulevel_first, menulevel_second, menulevel_third, url, created, updated):
        self.id = id
        self.website = website
        self.menulevel_first = menulevel_first
        self.menulevel_second = menulevel_second
        self.menulevel_third = menulevel_third
        self.url = url
        self.created = created
        self.updated = updated


class PageDataColumnEntity:
    def __init__(self, id, data_tab_id, col_name, col_type, col_type_length, col_description, check_col_name, is_file_column, is_primary_key, is_data_maintenance_pk, created, updated):
        self.id = id
        self.data_tab_id = data_tab_id
        self.col_name = col_name
        self.col_type = col_type
        self.col_type_length = col_type_length
        self.col_description = col_description
        self.check_col_name = check_col_name
        self.is_file_column = is_file_column
        self.is_primary_key = is_primary_key
        self.is_data_maintenance_pk = is_data_maintenance_pk
        self.created = created
        self.updated = updated


class PageDataConfEntity:
    def __init__(self, id, page_data_id, p_type, p_key, p_value, p_description, created, updated):
        self.id = id
        self.page_data_id = page_data_id
        self.p_type = p_type
        self.p_key = p_key
        self.p_value = p_value
        self.p_description = p_description
        self.created = created
        self.updated = updated


class PageDataEntity:
    def __init__(self, id, page_id, data_name, data_source_type, data_update_freq, data_update_time, created, updated):
        self.id = id
        self.page_id = page_id
        self.data_name = data_name
        self.data_source_type = data_source_type
        self.data_update_freq = data_update_freq
        self.data_update_time = data_update_time
        self.created = created
        self.updated = updated


class DataTabEntity:
    def __init__(self, id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated):
        self.id = id
        self.name = name
        self.page_data_id = page_data_id
        self.check_name_rule = check_name_rule
        self.business_columns = business_columns
        self.pre_cnt = pre_cnt
        self.created = created
        self.updated = updated
