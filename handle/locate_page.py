from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class LocatePage:
    def __init__(self, url):
        self.url = url

    def spider_page(self, port):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(port))
        web_driver = webdriver.Chrome(chrome_options=chrome_options)
        web_driver.get(self.url)
        return web_driver
