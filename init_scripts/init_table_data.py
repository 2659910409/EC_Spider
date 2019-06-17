from service.store_service import StoreService
from service.page_data_service import PageService, PageDataService
import pandas as pd
import numpy as np

if __name__ == '__main__':
    # 读取所有excel配置文件
    t_store = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_store.xlsx')
    t_store = t_store.where(t_store.notnull(), None)
    t_store_property = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_store_property.xlsx')
    t_store_property = t_store_property.where(t_store_property.notnull(), None)
    t_page = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_page.xlsx')
    t_page = t_page.where(t_page.notnull(), None)
    t_page_data = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_page_data.xlsx')
    t_page_data = t_page_data.where(t_page_data.notnull(), None)
    t_page_data_conf = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_page_data_conf.xlsx')
    t_page_data_conf = t_page_data_conf.where(t_page_data_conf.notnull(), None)
    t_data_tab = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_data_tab.xlsx')
    t_data_tab = t_data_tab.where(t_data_tab.notnull(), None)
    t_data_tab_column = pd.read_excel('D:/py3_project/EC_Spider/init_scripts/INIT_TABLE_DATA/t_data_tab_column.xlsx')
    t_data_tab_column = t_data_tab_column.where(t_data_tab_column.notnull(), None)
    # 遍历获取store批次数据
    t_store_list = np.array(t_store).tolist()
    t_page_list = np.array(t_page).tolist()
    for store in t_store_list:
        t_store_property_list = np.array(t_store_property[t_store_property['store_name'] == store[0]].iloc[:, 1:]).tolist()
        store_obj = StoreService().add_store(store[0], store[1], store[2], store[3], properties=t_store_property_list)
    # 遍历获取page批次
    for page in t_page_list:
        page_name = page[1]
        page_obj = PageService().add_page(page[0], page[1], page[2], page[3], page[4], page[5])
        t_page_data_list = np.array(t_page_data[t_page_data['page_name'] == page_name].iloc[:, 1:]).tolist()
        # 遍历获取page_data批次
        for page_data in t_page_data_list:
            page_data_name = page_data[0]
            t_page_data_conf_list = np.array(t_page_data_conf[t_page_data_conf['page_data_name'] == page_data_name].iloc[:, 1:]).tolist()
            t_data_tab_list = np.array(t_data_tab[t_data_tab['page_data_name'] == page_data_name].iloc[:, 1:]).tolist()
            # 遍历获取data_tab批次
            data_tabs = []
            for data_tab in t_data_tab_list:
                data_tab_name = data_tab[0]
                t_data_tab_column_list = np.array(t_data_tab_column[t_data_tab_column['data_tab_name'] == data_tab_name].iloc[:, 1:]).tolist()
                data_tab.append(t_data_tab_column_list)
                data_tabs.append(data_tab)
            # 准备参数
            page_data.extend([data_tabs, t_page_data_conf_list])
            # 插入数据
            page_data_obj = PageDataService().add_page_data(page_obj.id, page_data[0], page_data[1],
                                                            page_data[2], page_data[3], page_data[4],
                                                            page_data[5], page_data_confs=page_data[6])



