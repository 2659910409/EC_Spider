from handle.website.base import Base
from common.private_logging import Logging
from common.private_time import Time


class AccountDay(Base):
    def operation_page(self):
        self.driver.get('https://branding.taobao.com/#!/report/index?productid=101005202&effect=15&startdate=2019-06-05&enddate=2019-06-19')
        Time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="brix_12290"]/div[4]/a').click()
        Time.sleep(3)
        self.wait_download_finish()
        Logging.info(self.source_data_list)
        Logging.info('end')

    def operation_data_process(self):
        Logging.info(self.data_list)
        Logging.info('operation_data_process')


if __name__ == '__main__':
    store_id = 20
    page_data_id = 10
    port = 9000
    # step1:初始化爬虫任务所需的信息(统一)
    accountDay = AccountDay(store_id, page_data_id, port)
    # step2:页面操作含取数，获取：self.source_data/self.file_names（定制开发）
    accountDay.operation_page()
    # step3:数据处理（定制开发）
    accountDay.operation_data_process()
    # step4:数据入库(统一)
    # accountDay.operation_data_input()
    # step5:目前只针对下载文件 进行数据备份（针对文件下载类取数）(统一)
    # accountDay.operation_data_backup()
