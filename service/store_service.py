from dao.store_dao import StoreDAO
from dao.store_dao import StorePropertyDAO


class StoreService:
    def get_store(self, store_id):
        return StoreDAO(store_id)

    def get_stores(self, store_ids):
        stores = []
        for id in store_ids:
            _store = StoreDAO(id)
            if _store is not None:
                stores.append(_store)
        return stores


class StorePropertyService:
    def get_store_property(self, store_id):
        return StorePropertyDAO(store_id)

    def get_stores_property(self, stores_id):
        stores_property = []
        for store_id in stores_id:
            _stores_property = StoreDAO(store_id)
            if _stores_property is not None:
                stores_property.append(_stores_property)
        return stores_property
