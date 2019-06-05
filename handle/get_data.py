class GetData:
    def __init__(self, web_driver):
        self.web_driver = web_driver

    def get_service_basickpi(self):
        table_ele = self.web_driver.find_elements_by_xpath('//div[@class="th"]/div[@class="tbody"]')

    def get_service_kpi(self):
        category = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div[1]/span').text
        check_syn_score = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[1]/div[1]/div[1]').text
        market_onlist = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[1]/div[2]/div/div').text
        onlist_standard_1 = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[1]/div[2]/span').text
        only_refund_rate = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/span[3]').text
        refund_rate = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/span[3]').text
        store_evaul_button = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div[1]/div')
        store_evaul_button.click()
        syn_exp_star = driver.find_element_by_xpath('//*[@id="container"]//div[@class="detail"]/p').text
        syn_exp_score = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[2]/div[1]/div[1]/div[2]').text
        syn_exp_onlist = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[2]/div[1]/div[1]/div[3]').text
        onlist_standard_2 = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/span[2]').text



