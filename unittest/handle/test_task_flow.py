from handle.common.logging import Logging
from handle.err_message import ErrorEnum
from handle.task_controller import TaskController
from handle.task_parameters import TaskParameters


# step0.1:Master:全量任务生成
def worker_task_init():
    tc = TaskController('handle.task_creator.TaskCreator')
    tc.run('task_init')


# step0.2:Master:增量任务生成
def worker_task_added():
    tc = TaskController('handle.task_creator.TaskCreator')
    tc.run('task_added')


# step0.3:Worker:任务获取
def worker_task_run():
    tc = TaskController('handle.task_creator.TaskCreator')
    store_id, page_data_ids = tc.run('get_task')
    port = None
    for page_data_id in page_data_ids:
        # step1:Worker:取数-初始化任务
        params = TaskParameters(store_id, page_data_id, port)
        task = TaskController('handle.website.subway.report.SubReportDay', params)
        if not task.is_success():
            # 店铺未登录异常
            if task.error.name == ErrorEnum.ERROR_1001.name:
                # step2:Worker:取数-登录操作
                login_tc = TaskController('handle.login.tb_login.TaoLogin', task.store)
                login_tc.run('run')
                port = login_tc.port
        # step3:Worker:取数-页面操作
        task.run('operation_page')
        # step4:Worker:取数-页面文件下载及读取
        task.run('operation_page_download')
        # step5:Worker:取数-数据处理
        task.run('operation_data_process')
        # step6:Worker:取数-数据入库
        task.run('operation_data_input')
        # step7:Worker:取数-数据备份
        task.run('operation_data_backup')


if __name__ == '__main__':
    # 全量初始化任务执行
    worker_task_init()
    worker_task_run()
    # 增量初始化任务执行
    worker_task_added()
    worker_task_run()
