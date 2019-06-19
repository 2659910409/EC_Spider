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
        if self.page_data.is_multiple_data():
            # TODO 多个，待完善
            self.get_source_data_list()
            pass
        else:
            # step1：取有效数据列表
            start_position = '来源名称'
            source_data = self.get_source_data()
            get_data_flag = False
            data_cols = [] # 数据表title
            data_list = [] # 数据表内容
            for index, row in source_data.T.iteritems():
                values = row.values
                if get_data_flag:
                    data_list.append(values)
                if values[0] == start_position:
                    get_data_flag = True
                    data_cols = values
            if len(data_list) == 0:
                Logging.warning('无数据！')
                return True
            # step2：取所需数据列
            _data = []
            data_tab = self.page_data.data_tabs[0]
            conf_columns = data_tab.get_file_columns()
            conf_check_columns = data_tab.get_file_columns()
            intersection_col = []
            data_col_ind = []
            for col in conf_check_columns:
                if col in data_cols:
                    data_col_ind.append(data_cols.index(col))
                    intersection_col.append(col)
            for d in data_list:
                _row = []
                for ind in data_col_ind:
                    col_name = intersection_col[ind]
                    col_val = d[ind]
                    if col_name in ['int', 'bigint', 'int32', 'int64', 'tinyint', 'integer']:
                        _col_val = self.str_to_int(col_val)
                    elif col_name in ['float', 'numeric', 'decimal', 'double']:
                        _col_val = self.str_to_float(col_val)
                    elif col_name in ['varchar', 'string']:
                        _col_val = self.str_to_int(col_val)
                    else:
                        _col_val = col_val
                    _row.append(_col_val)
                _data.append(_row)
            # 数据列校验, TODO 监控告警
            tmp_surplus = list(set(data_cols) - set(conf_columns)) # 新增字段/列
            tmp_defect = list(set(conf_columns) - set(data_cols)) # 缺少字段/列
            Logging.warning('字段列匹配，原始字段列表：', data_cols) if len(tmp_surplus+tmp_defect) > 0 else None
            Logging.warning('字段列匹配，配置字段列表：', conf_columns) if len(tmp_surplus+tmp_defect) > 0 else None
            Logging.warning('字段列匹配，新增字段/列：', tmp_surplus) if len(tmp_surplus) > 0 else None
            Logging.warning('字段列匹配，缺少字段/列：', tmp_defect) if len(tmp_defect) > 0 else None
            # DataFrame生成
            import pandas as pd
            df = pd.DataFrame(_data, columns=intersection_col)
            # TODO 公共列增加
            df['店铺id'] = self.store.id
            df['店铺'] = self.store.name
            df['日期'] = get_yesterday()
            df['取数时间'] = get_current_date('%Y-%m-%d %H:%M:%S')
            df['入库时间'] = get_current_date('%Y-%m-%d %H:%M:%S')
            self.data_list.append(df)

    def operation_data_input(self):
        # TODO 匹配字段入库
        if self.page_data.is_multiple_data():
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
    # "chrome.exe" --profile-directory="Profile 1001" --remote-debugging-port=9000 --user-data-dir="C:/Users/jjshi/Downloads/chrome_user/1001"
    # step2：浏览器输入生意参谋url，并登录生意参谋成功**
    # url：https://sycm.taobao.com/portal/home.htm
    # step3：启动python程序，可进行取数开发
    store_id = 1
    page_data_id = 3
    port = 9000
    # step3.1：任务初始化（统一操作）
    flow_day = FlowDay(store_id, page_data_id, port)
    # step3.2：页面操作、下载文件、读取文件内容（定制开发）
    flow_day.operation_page()
    # step3.3：数据处理（定制开发）
    flow_day.operation_data_process()
    # step3.4：数据入库（统一操作）
    flow_day.operation_data_input()
    # step3.5：数据备份（统一操作）
    flow_day.operation_data_backup()
