from service.store_service import StoreService


def query_store():
    pass


def delete_store(store_id):
    pass


def add_store(store_param):
    store_service = StoreService()
    store_service.add_store(store_param[0], store_param[1], store_param[2], store_param[3], store_param[4])


if __name__ == '__main__':
    store_name = 'CeraVe适乐肤官方旗舰店'
    store_param = [store_name, '淘宝', '431052811', 'cerave适乐肤官方旗舰店:sycm', [['tf_param', 'exec_chrome_command', '"chrome.exe" --profile-directory="Profile 1001" --user-data-dir="C:/RPAData/chrome_user/1001_HAIR"', '指定chrome浏览器启动命令']]]
    store_ = add_store(store_param)
    store = query_store(store_.store_id)
    if not store:
        assert '插入失败，未找到店铺'
    if store.name != store_name:
        assert '插入失败，店铺信息不匹配'
    delete_store(store_.store_id)
    store = query_store(store_.store_id)
    if store:
        assert '店铺删除失败，找到店铺'
