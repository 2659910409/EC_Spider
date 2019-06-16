from common.db import DB
from dao.store_dao import StoreDao, StorePropertyDao
from entity.store import StoreEntity, StorePropertyEntity
from common.private_logging import Logging


class StoreService:
    def get_store(self, store_id):
        """
        获取单个店铺对象
        :param store_id: 店铺id
        :return: 店铺实体对象
        """
        data = StoreDao().query(store_id)
        if data:
            data = data[0]
            property_entity = self._get_store_properties(store_id)
            store = StoreEntity(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], property_entity)
            return store
        else:
            Logging.error('店铺id不存在:', store_id)

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

    def _get_store_properties(self, store_id):
        """
        获取店铺的属性列表
        :param store_id: 店铺id
        :return: 返回该店铺所有属性组成的二维数组
        """
        data = StorePropertyDao().query_by_store_id(store_id)
        if data:
            store_properties = []
            for row in data:
                store_properties.append(StorePropertyEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            return store_properties
        else:
            Logging.error('该店铺id不存在:', store_id)

    def check_store_name_exists(self, store_name):
        """根据店铺名验证店铺是否已存在"""
        data = StoreDao().query_by_name(store_name)
        if data:
            return True
        else:
            return False

    def add_store(self, name, plt_name, plt_store_id, login_username=None, url=None, status=1, properties=None):
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
            Logging.error('add_store：', name, '店铺名已存在！')
            return None
        key = StoreDao().insert(name, plt_name, plt_store_id, login_username, url, status)
        if properties:
            for x in properties:
                StorePropertyDao().insert(key, x[0], x[1], x[2], x[3])
        store = self.get_store(key)
        return store

    def delete_store(self, store_id):
        StorePropertyDao().delete_by_store_id(store_id)
        StoreDao().delete(store_id)










