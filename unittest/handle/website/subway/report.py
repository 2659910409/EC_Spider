from handle.website.subway.report import SubReportDay
from service.store_service import StoreService
from handle.website.subway.report import SubReport

# def get_task(queue):
#     return queue.pop(0)

if __name__ == '__main__':
    subreport = SubReport('皇家美素佳儿旗舰店', '123', 9001)
    subreport.get_webdriver()
    subreport.web_driver
    pass


# if __name__ == '__main__':
#     # 1、Master任务初始化
#     queue = [[1, 2], [1, 3]]
#     # 2、Worker获取任务
#     store_id, page_data_id = get_task(queue)
#     # 3、初始化任务
#     store_id = None
#     store = StoreService.get_store(store_id)
#     page_data = None
#     port = None
#     srd = SubReportDay(store, page_data)
#     # 4、login
#     port = None
#     srd.set_webdriver(port)
#     # 5、页面操作
#     srd.operation_page()
#     # 6、页面文件下载
#     srd.operation_page_download()
#     # 7、数据读取与处理
#     srd.operation_data_process()
#     # 8、数据入库
#     srd.operation_data_input()
#     # 9、数据文件备份/管理
#     if not srd.operation_data_backup():
#         print(srd.error)
