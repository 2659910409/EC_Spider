from handle.website.base import Base
from common.private_time import Time
from common.private_logging import Logging
from common.util_time import get_yesterday, get_current_date


class Flow(Base):

    def _operation_page_load(self, start_date, end_date, date_type, item_id):
        """
        入参：日期区间 例:'2019-05-24', '2019-05-24', 'day'
        :param start_date:
        :param end_date:
        :param date_type:
        :param item_id:
        :return:
        """
        base_url = "https://sycm.taobao.com/cc/item_archives?activeKey=flow&dateRange={}|{}&dateType={}&itemId={}"
        target_url = base_url.format(start_date, end_date, date_type, item_id)
        self.driver.get(target_url)
        # 等待页面加载完成
        Time.sleep(6)

    def operation_data_process(self):
        if self.page_data.is_multiple_tab():
            # TODO 多个，待完善
            self.get_source_data_list()
            pass
        else:
            # step1：根据启始位置，获取有效数据
            starting_position = '来源名称'
            source_df = self.get_source_data()
            pro_df = self.df_effective_by_starting_position(starting_position, source_df)
            # step2：取所需数据列，数据类型转换
            data_tab = self.page_data.data_tabs[0]
            df = self.df_data_process(data_tab, pro_df)
            # step3：DataFrame添加公共字段
            df['店铺id'] = self.store.id
            df['店铺'] = self.store.name
            df['日期'] = get_yesterday()
            if self.page_data.is_file_download():
                df['文件路径'] = self.get_file_path_effective()
                df['文件sheet'] = self.get_file_name()
                # TODO 获取文件时间戳
                df['取数时间'] = get_current_date('%Y-%m-%d %H:%M:%S')
            else:
                df['取数时间'] = get_current_date('%Y-%m-%d %H:%M:%S')
            df['入库时间'] = get_current_date('%Y-%m-%d %H:%M:%S')
            self.data_list.append(df)

    def operation_data_input(self):
        # TODO 匹配字段入库
        if self.page_data.is_multiple_tab():
            # TODO 多个，待完善
            self.get_data_list()
            pass
        else:
            df = self.get_data()
            tab = self.page_data.data_tabs[0]
            # del_condition 删除条件拼接: 店铺id = '1' and 日期 = '2019-06-18'
            del_condition = self.gen_data_maintenane_condition(tab, df)
            del_sql = 'DELETE FROM {} WHERE {};'.format(tab.name, del_condition)
            # cols_part 字段列表拼接: id,name
            cols_part = ','.join(df.columns)
            # data_part 数据列表拼接: (1,'zhangsan'),(2,'lisi'),(3,'wangwu')
            data_part = self.gen_data_insert_values(tab, df)
            insert_sql = 'INSERT INTO {} ({}) VALUES {};'.format(tab.name, cols_part, data_part)
            self.db.execute(del_sql)
            self.db.execute(insert_sql)
            self.db.commit()


class FlowDay(Flow):

    def operation_page(self):
        start_date = get_yesterday()
        end_date = start_date
        date_type = 'day'
        # item_id = '551562733140'
        item_id = '546299843179'
        self._operation_page_load(start_date, end_date, date_type, item_id)
        # 点击下载按钮
        self.driver.find_element_by_xpath('//*[@id="op-cc-item-archives-flow-flow-origin"]/div[1]/div[1]/div[2]/a/span').click()
        # 等待文件下载完成
        self.data_dimension_dict['{item_id}'] = item_id # 商品id特殊处理
        self.wait_download_finish()
        # 维护商品id字段
        self.source_data_list[0]['商品id'] = item_id # 商品id特殊处理


class FlowMonth(Flow):

    def operation_page(self):
        # TODO
        start_date = None
        end_date = None
        date_type = 'month'
        item_id = '551562733140'
        self._operation_page_load(start_date, end_date, date_type, item_id)
        # 点击下载按钮
        self.driver.find_element_by_xpath('//*[@id="op-cc-item-archives-flow-flow-origin"]/div[1]/div[1]/div[2]/a/span').click()
        # 文件匹配前缀，不需要设置
        self.page_data.rule_read_file_prefix = '【生意参谋平台】无线商品二级流量来源详情'
        # 等待文件下载完成
        data_dimension_dict = {'{item_id}': item_id}
        self.wait_download_finish(data_dimension_dict)
        # 维护商品id字段
        df = self.source_data_list[0]['商品id'] = item_id


if __name__ == '__main__':
    # step1：cmd运行命令行，执行如下
    # 测试店铺1 端口9000：chrome.exe --profile-directory="Profile 1020" --remote-debugging-port=9000 --user-data-dir="C:/RPAData/chrome_user/1020_LP" --start-maximized https://sycm.taobao.com/custom/login.htm
    # 测试店铺2 端口9001：chrome.exe --profile-directory="Profile 1021" --remote-debugging-port=9001 --user-data-dir="C:/RPAData/chrome_user/1021_KS" - -start - maximized https: // sycm.taobao.com / custom / login.htm
    # shijun: "chrome.exe" --profile-directory="Profile 1001" --remote-debugging-port=9000 --user-data-dir="C:/Users/jjshi/Downloads/chrome_user/1001"
    # step2：浏览器输入生意参谋url，并登录生意参谋成功**
    # url：https://sycm.taobao.com/portal/home.htm
    # step3：启动python程序，可进行取数开发
    store_id = 1
    page_data_id = 3
    port = 9000
    # step3.1：任务初始化（统一操作）
    flow_day = FlowDay(store_id, page_data_id, port)
    # step3.2：页面操作、下载文件、读取文件内容（定制开发）,维度：self.source_data_list
    flow_day.operation_page()
    # step3.3：数据处理（定制开发），维护：self.data_list
    flow_day.operation_data_process()
    # step3.4：数据入库（统一操作）
    flow_day.operation_data_input()
    # step3.5：数据备份（统一操作）
    flow_day.operation_data_backup()
