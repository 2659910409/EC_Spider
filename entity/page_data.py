
class PageEntity:
    def __init__(self, id, website, name, menu_level_first, menu_level_second, menu_level_third, url, created, updated):
        self.id = id
        self.website = website
        self.name = name
        self.menu_level_first = menu_level_first
        self.menu_level_second = menu_level_second
        self.menu_level_third = menu_level_third
        self.url = url
        self.created = created
        self.updated = updated


class DataTabColumnEntity:
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
    def __init__(self, id, page_id, name, status, data_source_type, data_update_freq, data_update_time, created, updated, page_data_confs, page, data_tabs):
        self.id = id
        self.page_id = page_id
        self.name = name
        self.status = status
        self.data_source_type = data_source_type
        self.data_update_freq = data_update_freq
        self.data_update_time = data_update_time
        # TODO 是否是下载取数
        self.is_download = False
        # TODO 多张物理表、多个数据/多个文件
        self.is_multiple_data = False
        self.created = created
        self.updated = updated
        self.page_data_confs = page_data_confs
        self.page = page
        self.data_tabs = data_tabs

    def is_download_file(self):
        if self.data_source_type == 'file':
            return True
        elif self.data_source_type == 'html':
            return False
        else:
            raise Exception('未知的源数据类型 data_source_type:', self.data_source_type)


class DataTabEntity:
    def __init__(self, id, name, page_data_id, check_name_rule, business_columns, pre_cnt, created, updated, data_tab_columns):
        self.id = id
        self.name = name
        self.page_data_id = page_data_id
        self.check_name_rule = check_name_rule
        self.business_columns = business_columns
        self.pre_cnt = pre_cnt
        self.created = created
        self.updated = updated
        self.data_tab_columns = data_tab_columns
