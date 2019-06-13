from service.store_service import StoreService
from dao.store_dao import StoreDao
from common.db import DB


if __name__ == '__main__':
    store_service = StoreService()
    result = store_service.add_store(name='CeraVe适乐肤官方旗舰店', plt_name='淘宝', plt_store_id='431052811',login_username='cerave适乐肤官方旗舰店:sycm',
                                     properties=[['tf_param', 'exec_chrome_command', '"chrome.exe" --profile-directory="Profile 1001" --user-data-dir="C:/RPAData/chrome_user/1001_HAIR"', '指定chrome浏览器启动命令']])

    DB().dispose()

    # store_dao = StoreDao().query_by_name('CeraVe适乐肤官方旗舰店')
    # print(store_dao)

