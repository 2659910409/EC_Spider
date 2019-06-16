from service.page_data_service import PageDataService, PageService, DataTabService
import unittest


class TestPageService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("类执行之前的方法")

    @classmethod
    def tearDownClass(cls):
        print("类执行之后的方法")

    # 每次方法之前执行
    def setUp(self):
        print('测试用例执行前的环境准备')

    # 每个方法之后执行
    def tearDown(self):
        print('测试用例执行后的环境清理')

    @unittest.skip("我想临时跳过这个文件")
    def test_add_page(self):
        page_param = ['直通车', '报表', 'https://subway.simba.taobao.com/#!/report/bpreport/index', '直通车报表']
        page_service = PageService()
        page = page_service.add_page(page_param[0], page_param[1], page_param[2], menu_level_second=page_param[3])
        self.assertIsNotNone(page, '插入失败,未返回page对象')
        page_new = page_service.get_page(page.id)
        self.assertEqual(page_param[2], page_new.url, '插入失败,page的url信息不匹配')

    @unittest.skip("我想临时跳过这个文件")
    def test_get_page(self):
        page_id = 1
        page_url = 'https://subway.simba.taobao.com/#!/report/bpreport/index'
        page_service = PageService()
        page = page_service.get_page(page_id)
        self.assertIsNotNone(page, '未找到page')
        self.assertEqual(page_url, page.url, '获取page的url信息与实际url不匹配')


class TestPageDataService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("类执行之前的方法")

    @classmethod
    def tearDownClass(cls):
        print("类执行之后的方法")

    # 每次方法之前执行
    def setUp(self):
        print('测试用例执行前的环境准备')

    # 每个方法之后执行
    def tearDown(self):
        print('测试用例执行后的环境清理')

    @unittest.skip("我想临时跳过这个文件")
    def test_add_page_data(self):
        page_data_param = [1, '推广计划列表-宝贝-日报', 'file', 'day', '每天12:00更新',
                           [['筛选条件', '转化周期', '15天累计数据', '维度条件:转化周期']]]
        page_data_service = PageDataService()
        page_data = page_data_service.add_page_data(page_data_param[0], page_data_param[1], page_data_param[2], page_data_param[3], page_data_param[4], page_data_confs=page_data_param[5])

        self.assertIsNotNone(page_data, '插入失败,未返回page对象')
        page_data_new = page_data_service.get_page_data(page_data.id)
        self.assertEqual(page_data_param[1], page_data_new.name, '插入失败,page_data的data_name信息不匹配')

    @unittest.skip("我想临时跳过这个文件")
    def test_get_page_data(self):
        page_data_id = 8
        data_name = '推广计划列表-宝贝-日报'
        page_data_service = PageDataService()
        page_data = page_data_service.get_page_data(page_data_id)
        self.assertIsNotNone(page_data, '未找到page')
        self.assertEqual(data_name, page_data.name, '获取page_data的name信息与实际url不匹配')

    # @unittest.skip("我想临时跳过这个文件")
    def test_add_data_tab(self):
        page_data_id = 8
        data_tab_param = ['app_subway_report_spreadbaby_day', page_data_id, '平台-页面-菜单-模块-粒度', '店铺id,日期,转化周期',
                          [[]]]



if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # test_cases = [TestStoreService("test_add_store"),
    #               TestStoreService("test_get_store"),
    #               TestStoreService("test_check_store_name_exists"),
    #               TestStoreService("test_delete_store")]
    # suite.addTests(test_cases)
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)

# if __name__ == '__main__':
#     # page_service = PageService()
#     # test2 = page_service.add_page('直通车', '报表', 'https://subway.simba.taobao.com/#!/report/bpreport/index', '直通车报表')
#     # page_data_service = PageDataService()
#     # test1 = page_data_service.add_page_data(1, '推广计划列表-宝贝-日报', 'file', 'day', '每天12:00更新')
#     data_tab_service = DataTabService()
#     test1 = data_tab_service.add_data_tab('app_subway_spread_baby_day', '推广计划列表-宝贝-日报', 'file', 'day', '每天12:00更新')
#
#     DB().dispose()
#
#     # store_dao = StoreDao().query_by_name('CeraVe适乐肤官方旗舰店')
#     # print(store_dao)