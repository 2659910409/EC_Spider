from handle.website.base import Base
from handle.common import time


class Flow(Base):

    def _operation_page_load(self, start_date, end_date, date_type, item_id):
        """
        入参：日期区间，每个元素是一个字符串，例 ['2019-05-24', '2019-05-24', 'day']
        :param start_date:
        :param end_date:
        :param date_type:
        :param item_id:
        :return:
        """
        base_url = "https://sycm.taobao.com/cc/item_archives?activeKey=flow&dateRange={}|{}&dateType={}&itemId={}"
        target_url = base_url.format(start_date, end_date, date_type, item_id)
        self.driver.get(target_url)
        time.sleep(5)

    def operation_page(self):
        start_date = time.get_yesterday()
        end_date = start_date
        date_type = 'day'
        item_ids = []
        for item_id in item_ids:
            self._operation_page_load(start_date, end_date, date_type, item_id)
            # 点击下载按钮
            self.driver.find_element_by_xpath('//*[@id="op-cc-item-archives-flow-flow-origin"]/div[1]/div[1]/div[2]/a/span').click()
            # TODO 可配置变量
            file_prefix = ''
            # 保存文件目录规则
            file_path_suffix = item_id
            # 等待文件下载完成
            self.wait_download_finish(file_prefix, file_path_suffix)

    def operation_data_process(self):
        df = None
        for data in self.get_source_data_list():
            # TODO data公共列增加
            # TODO 字段类型转换
            if df is None:
                df = data
            else:
                df = df.merge(data)
        self.data_list.append(df)

    def operation_data_input(self):
        # TODO 字段匹配入库
        self.get_data()

