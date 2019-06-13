from service.page_data_service import PageDataService, PageService, DataTabService
from dao.page_data_dao import PageDataDao
from common.db import DB


if __name__ == '__main__':
    # page_service = PageService()
    # test2 = page_service.add_page('直通车', '报表', 'https://subway.simba.taobao.com/#!/report/bpreport/index', '直通车报表')
    # page_data_service = PageDataService()
    # test1 = page_data_service.add_page_data(1, '推广计划列表-宝贝-日报', 'file', 'day', '每天12:00更新')
    data_tab_service = DataTabService()
    test1 = data_tab_service.add_data_tab('app_subway_spread_baby_day', '推广计划列表-宝贝-日报', 'file', 'day', '每天12:00更新')

    DB().dispose()

    # store_dao = StoreDao().query_by_name('CeraVe适乐肤官方旗舰店')
    # print(store_dao)