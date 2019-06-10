from dao.page_data_dao import PageDataDao
from dao.page_data_dao import PageDao


class PageService:
    def __init__(self):
        pass

    def get_page(self, page_id):
        return PageDao(page_id)

    def get_pages(self, pages_id):
        pages = []
        for page_id in pages_id:
            _page = PageDao(page_id)
            if _page is not None:
                pages.append(_page)
        return pages


class PageDataService:
    def __init__(self):
        pass

    def get_page_data(self, page_data_id):
        return PageDataDao(page_data_id)

    def get_pages_data(self, pages_data_id):
        pages_data = []
        for page_data_id in pages_data_id:
            _page = PageDao(page_data_id)
            if _page is not None:
                pages_data.append(_page)
        return pages_data

