from service.page_data_service import PageDataService, PageService
import unittest


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

    # @unittest.skip("我想临时跳过这个文件")
    def test_page_data(self):
        # 插入page数据并返回一个page对象
        page_param = ['直通车', '报表-直通车报表', '报表', '直通车报表', None, 'https://subway.simba.taobao.com/#!/report/bpreport/index']
        page_service = PageService()
        page = page_service.add_page(page_param[0], page_param[1], page_param[2], page_param[3], page_param[4], page_param[5])
        self.assertIsNotNone(page, '插入失败,未返回page对象')
        page_new = page_service.get_page(page.id)
        self.assertEqual(page_param[5], page_new.url, '插入失败,page的url信息不匹配')
        # 插入page_data数据，并返回一个page_data对象
        data_tab_columns = [['花费_分_', 'bigint', None, '花费_分_', '花费(分)', 1, 0, 0],
                             ['点击率', 'decimal', '18,2', '点击率', '点击率(%)', 1, 0, 0]]
        data_tabs = [['app_subway_spread_baby_day', '直通车-推广计划列表-宝贝', '日期', 1, data_tab_columns]]
        page_data_confs = [['筛选条件', '转化周期', '15天累计数据', '条件:转化周期'],
                           ['筛选条件', '报表类型', '宝贝', '条件:宝贝']]
        page_data_param = [page_new.id, '推广计划列表-宝贝-日报', 1, 'file', 'day', '12:00', None, None, data_tabs, page_data_confs]
        page_data_service = PageDataService()
        page_data = page_data_service.add_page_data(page_data_param[0], page_data_param[1], page_data_param[2],
                                                    page_data_param[3], page_data_param[4], page_data_param[5],
                                                    page_data_param[6], page_data_param[7], page_data_param[8],
                                                    page_data_confs=page_data_param[9])
        self.assertIsNotNone(page_data, '插入失败,未返回page_data对象')
        # 查询获取page_data对象与原数据进行对比验证
        page_data_new = page_data_service.get_page_data(page_data.id)
        self.assertEqual(page_data_param[1], page_data_new.name, '插入失败,page_data的name信息不匹配')
        if page_data_confs is not None:
            self.assertIsNotNone(page_data.page_data_confs, '插入失败,未返回page_data_conf对象')
        self.assertIsNotNone(page_data.data_tabs, '插入失败,未找到data_tab信息')
        data_tab = page_data.data_tabs[0]
        self.assertEqual(data_tabs[0][0], data_tab.name, '插入失败,data_tab的name信息不匹配')
        self.assertIsNotNone(data_tab.data_tab_columns, '插入失败,未找到data_tab_column信息')
        page_data_result = page_data_service.delete_page_data(page_data_new.id)
        self.assertIsNone(page_data_result, '删除失败,page_data未被删除')
        self.assertIsNone(page_data_service._get_data_tabs(page_data_new.id), '删除失败,data_tabs未被删除')
        self.assertIsNone(page_data_service._get_data_tab_columns(page_data_new.data_tabs[0].id), '删除失败,data_tab_columns未被删除')
        self.assertIsNone(page_data_service._get_page_data_confs(page_data_new.id), '删除失败,page_data_confs未被删除')


if __name__ == '__main__':
    unittest.main()


