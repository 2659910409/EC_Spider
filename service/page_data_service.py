from dao.page_data_dao import PageDataDao
from dao.page_data_dao import PageDao


class PageService:

    def get_page(self, page_id):
        return PageDao(page_id)

    def get_pages(self, page_ids):
        pages = []
        for page_id in page_ids:
            _page = PageDao(page_id)
            if _page is not None:
                pages.append(_page)
        return pages


class PageDataService:

    def get_page_data(self, page_data_id):
        return PageDataDao(page_data_id)

    def get_columns(self, page_data):
        columns = []
        for x in page_data.page_data_columns:
            columns.append(x.col_name)
        return columns

    def get_file_columns(self, page_data):
        columns = []
        for x in page_data.page_data_columns:
            if x.is_file_column == 1:
                columns.append(x.col_name)
        return columns

    def set_file_column_flag(self, page_data, columns):
        """
        文件title 与 配置表所需字段匹配，匹配到为存在，设置is_exists_file = True
        :param columns: file title列表
        :return: True
        """
        for f_col_name in columns:
            for t_col in page_data.page_data_columns:
                if t_col.check_col_name == f_col_name:
                    t_col.is_exists_file = True
        return page_data

    def get_file_exists_columns(self, page_data):
        columns = []
        for t_col in self.page_data.page_data_columns:
            if t_col.is_exists_file == 1:
                columns.append(t_col.col_name)
        return columns
