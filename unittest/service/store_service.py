from service.store_service import StoreService
import unittest


class TestStoreService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("类执行之前的方法")

    @classmethod
    def tearDownClass(cls):
        print("类执行之后的方法")

    # 每次方法之前执行
    def setUp(self):
        pass

    # 每个方法之后执行
    def tearDown(self):
        pass

    @unittest.skip("我想临时跳过这个文件")
    def test_add_store(self):
        store_name = 'CeraVe适乐肤官方旗舰店'
        store_param = [store_name, '淘宝', '431052811', 'cerave适乐肤官方旗舰店:sycm', [['tf_param', 'exec_chrome_command','"chrome.exe" --profile-directory="Profile 1001" --user-data-dir="C:/RPAData/chrome_user/1001_HAIR"', '指定chrome浏览器启动命令']]]
        store_service = StoreService()
        store = store_service.add_store(store_param[0], store_param[1], store_param[2], login_username=store_param[3], properties=store_param[4])
        self.assertIsNotNone(store, '插入失败,未返回店铺对象')
        store_new = store_service.get_store(store.id)
        self.assertEqual(store_name, store_new.name, '插入失败，店铺信息不匹配')

    def test_get_store(self):
        store_id = 29
        store_name = 'CeraVe适乐肤官方旗舰店'
        store_service = StoreService()
        store = store_service.get_store(store_id)
        self.assertIsNotNone(store, '该店铺id不存在')
        self.assertEqual(store_name, store.name, '查询与实际店铺名不符')

    def test_check_store_name_exists(self):
        store_name = 'CeraVe适乐肤官方旗舰店'
        store_service = StoreService()
        r = store_service.check_store_name_exists(store_name)
        self.assertTrue(r, '检验错误,店铺实际存在,但检验结果为不存在')

    def test_delete_store(self):
        store_id = 29
        store_service = StoreService()
        store_service.delete_store(store_id)
        r_store = store_service.get_store(store_id)
        r_store_property = store_service.get_store_properties(store_id)
        self.assertFalse(r_store and r_store_property, '店铺或店铺属性未删除成功')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    test_cases = [TestStoreService("test_add_store"),
                  TestStoreService("test_get_store"),
                  TestStoreService("test_check_store_name_exists"),
                  TestStoreService("test_delete_store")]
    suite.addTests(test_cases)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)




