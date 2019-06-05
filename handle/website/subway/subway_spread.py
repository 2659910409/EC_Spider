class Base:
    def __init__(self, trans_period, date_level):
        self.trans_period = trans_period
        self.date_level = date_level

    def take_over(self, port):
        pass


class GetData(Base):
    def __init__(self, web_driver):
        self.web_driver = web_driver

    def locate_page(self, url):
        pass

    def filter_condition(self):
        pass

    def get_data(self):
        pass


class ParseFile:
    pass


class DataInput:
    pass