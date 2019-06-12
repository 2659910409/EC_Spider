from common.db import DB
from dao.store_dao import StoreDao, StorePropertyDao
from entity.store import StoreEntity, StorePropertyEntity


class StoreService:
    def get_store(self, store_id):
        """
        获取单个店铺对象
        :param store_id: 店铺id
        :return: 店铺实体对象
        """
        data = StoreDao.query_by_id(store_id)
        if data:
            id = data[0]
            name = data[1]
            plt_name = data[2]
            plt_store_id = data[3]
            login_username = data[4]
            url = data[5]
            status = data[6]
            created = data[7]
            updated = data[8]
            store = StoreEntity(id, name, plt_name, plt_store_id, login_username, url, status, created, updated)
            return store
        else:
            print('店铺id不存在:', store_id)

    def get_stores(self, store_ids):
        """
        获取多个店铺对象
        :param store_ids: 店铺id组成的列表
        :return: 店铺实体对象组成的列表
        """
        stores = []
        for store_id in store_ids:
            _store = self.get_store(store_id)
            if _store:
                stores.append(_store)
        return stores

    def get_store_properties(self, store_id):
        """
        获取店铺的属性列表
        :param store_id: 店铺id
        :return: 返回该店铺所有属性组成的二维数组
        """
        data = StorePropertyDao.query_by_store_id(store_id)
        if data:
            store_properties = []
            for row in data:
                id = row[0]
                store_id = row[1]
                p_type = row[2]
                p_key = row[3]
                p_value = row[4]
                p_description = row[5]
                created = row[6]
                updated = row[7]
                store_properties.append(StorePropertyEntity(id, store_id, p_type, p_key, p_value, p_description, created, updated))
            return store_properties
        else:
            print('该店铺id不存在:', store_id)

    def delete_store_by_id(self, store_id):
        """根据店铺id删除店铺"""
        symbol = StoreDao.delete_by_id(store_id)
        return symbol

    def check_store_name_exists(self, store_name):
        """根据店铺名验证店铺是否已存在"""
        data = StoreDao.query_by_name(store_name)
        if data:
            return True
        else:
            return False

    def add_store(self, name, plt_name, plt_store_id, login_username=None, url=None, status=1, properties=[]):
        """
        增加店铺
        :param name: 店铺名
        :param plt_name: 平台名
        :param plt_store_id: 平台店铺id
        :param login_username: 登录名
        :param url: 登录地址
        :param status: 店铺状态,设置为1，代表有效;设置为0,代表无效
        :param properties: 店铺属性列表,该参数需要传入二维数组
        :return:
        """
        if self.check_store_name_exists(name):
            raise Exception('该店铺名已存在:', name)
        else:
            StoreDao.insert(name, plt_name, plt_store_id, login_username, url, status)
            if properties:
                for x in properties:
                    StorePropertyDao(x[0], x[1], x[2], x[3], x[4])
            return True










