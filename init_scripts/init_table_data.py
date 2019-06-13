from service.store_service import StoreService
from service.page_data_service import PageService
from service.page_data_service import PageDataService
# Store初始化
stores = []
stores.append(['CeraVe适乐肤官方旗舰店', '淘宝', '431052811', 'cerave适乐肤官方旗舰店:sycm', [['tf_param', 'exec_chrome_command', '"chrome.exe" --profile-directory="Profile 1001" --user-data-dir="C:/RPAData/chrome_user/1001_HAIR"', '指定chrome浏览器启动命令']]])
store_service = StoreService()
for store in stores:
    store_service.add_store(store[0], store[1], store[2], store[3], store[4])

# Page初始化
# PageService.add_page()

# PageData
page_datas = []
data_tabs = []
page_data_confs = []
page_data_confs.append([])
data_tab_columns = []
data_tab_columns.append([])
data_tabs.append(['tab_1',data_tab_columns])
data_tab_columns = []
data_tab_columns.append([])
data_tabs.append(['tab_2',data_tab_columns])
page_datas.append([1, 'name', '', page_data_confs, data_tabs])
for page_data in page_datas:
    PageDataService.add_page_data(page_data)


