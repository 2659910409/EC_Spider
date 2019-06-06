import time
from timeout3 import time
from retry import retry
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Base:
    def __init__(self, trans_period, date_level):
        self.trans_period = trans_period
        self.date_level = date_level

    def take_over(self, port):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(port))
        web_driver = webdriver.Chrome(chrome_options=chrome_options)
        return web_driver


class GetData:
    def __init__(self, web_driver):
        self.web_driver = web_driver

    def locate_page(self, url):
        self.web_driver.get(url)

    def filter_condition(self):
        pass

    def get_data(self):
        pass


class ParseFile:
    def __init__(self, file_dir_path):
        self.file_dir_path = file_dir_path

    def find_file(self):
        pass

    def parse_file(self):
        pass


class DataInput:
    def __init__(self):
        pass

    def data_handle(self):
        pass


class DataBackUp:
    def __init__(self):
        pass
