from dao.page_data_dao import PageDataDao

class PageDataService:
    def __init__(self):
        pass

    def get_page_data(self, page_data_id):
        return PageDataDao(page_data_id)
