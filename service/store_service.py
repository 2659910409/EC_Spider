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

