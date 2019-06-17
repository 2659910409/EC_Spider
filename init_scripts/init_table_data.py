from service.store_service import StoreService
from service.page_data_service import PageService, PageDataService
import pandas as pd
import numpy as np

# Store
if __name__ == '__main__':
    # 读取所有excel配置文件
    t_store = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_store.xlsx')
    t_store_property = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_store_property.xlsx')
    t_page = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_page.xlsx')
    t_page_data = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_page_data.xlsx')
    t_page_data_conf = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_page_data_conf.xlsx')
    t_data_tab = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_data_tab.xlsx')
    t_data_tab_column = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_data_tab_column.xlsx')
    # 遍历获取store批次数据
    t_store_list = np.array(t_store).tolist()
    t_page_list = np.array(t_page).tolist()
    for store in t_store_list:
        store_name = store[0]
        t_store_property_list = np.array(t_store_property[t_store_property['store_name'] == store_name].iloc[:, 1:]).tolist()
    # 遍历获取page批次
    for page in t_page_list:
        page_name = page[1]
        t_page_data_list = np.array(t_page_data[t_page_data['page_name'] == page_name].iloc[:, 1:]).tolist()
        # 遍历获取page_data批次
        for page_data in t_page_data_list:
            page_data_name = page_data[1]
            t_page_data_conf_list = np.array(t_page_data_conf[t_page_data_conf['page_data_name'] == page_data_name].iloc[:, 1:]).tolist()
            t_data_tab_list = np.array(t_data_tab[t_data_tab['page_data_name'] == page_data_name].iloc[:, 1:]).tolist()
            # 遍历获取data_tab批次
            for data_tab in t_data_tab_list:
                data_tab_name = data_tab[1]
                t_data_tab_column_batch = np.array(t_data_tab_column[t_data_tab_column['data_tab_name'] == data_tab_name].iloc[:, 1:]).tolist()



# stores = []
# stores.append(['CeraVe适乐肤官方旗舰店', '淘宝', '431052811', 'cerave适乐肤官方旗舰店:sycm', [['tf_param', 'exec_chrome_command', 'chrome --profile-directory="Profile 1001" --user-data-dir="C:/RPAData/chrome_user/1001_HAIR"', '指定chrome浏览器启动命令']]])
# store_service = StoreService()
# for store in stores:
#     store_service.add_store(store[0], store[1], store[2], store[3], store[4])
#
# # Page初始化
# # PageService.add_page()
#
# # PageData
# page_datas = []
# data_tabs = []
# page_data_confs = []
# page_data_confs.append([])
# data_tab_columns = []
# data_tab_columns.append([])
# data_tabs.append(['tab_1',data_tab_columns])
# data_tab_columns = []
# data_tab_columns.append([])
# data_tabs.append(['tab_2',data_tab_columns])
# page_datas.append([1, 'name', '', page_data_confs, data_tabs])
# for page_data in page_datas:
#     PageDataService.add_page_data(page_data)


