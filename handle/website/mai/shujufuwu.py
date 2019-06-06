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
        self.web_driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div/div/span/input').clear()
        self.web_driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div/div/span/input').send_keys("2019-06-04")

    def get_data(self):
        # table_ele = driver.find_elements_by_xpath('//div[@class="th"]/div[@class="tbody"]')
        category = self.web_driver.find_element_by_xpath('//*[@id="container"]//div[@class="category"]/span').text
        check_syn_score = self.web_driver.find_element_by_xpath('//*[@id="container"]//div[@class="headline"]/div[@class="score"]').text
        market_onlist = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[1]/div[2]/div/div').text
        onlist_standard_1 = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[1]/div[2]/span').text
        only_refund_rate = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/span[3]').text
        refund_rate = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/span[3]').text
        store_evaul_button = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div[1]/div')
        store_evaul_button.click()
        syn_exp_star = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[1]/div[2]/div[2]/div/p/text()')
        syn_exp_score = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[2]/div[1]/div[1]/div[2]').text
        syn_exp_onlist = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[2]/div[1]/div[1]/div[3]').text
        onlist_standard_2 = self.web_driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/span[2]').text



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
