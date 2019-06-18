from handle.task_controller import TaskController
from common.private_logging import Logging


# step0.1:Master:全量任务生成
def worker_task_init():
    tc = TaskController('handle.task_creator.TaskCreator')
    tc.run('task_init')


# step0.2:Master:增量任务生成
def worker_task_added():
    tc = TaskController('handle.task_creator.TaskCreator')
    tc.run('task_added')


def worker_task_finish():
    tc = TaskController('handle.task_creator.TaskCreator')
    tc.run('task_finish')


# step0.3:Worker:任务获取
def worker_task_run():
    tc = TaskController('handle.task_creator.TaskCreator')
    job_id, store_id, page_data_ids = tc.run('get_task')
    while job_id:
        flag = tc.run('task_set_start', {'job_id': job_id})
        # 任务获取成功
        if not flag:
            # 继续获取任务
            Logging.info('job:', job_id, store_id, page_data_ids, ' 任务领取慢了一拍，继续获取其他任务！')
            job_id, store_id, page_data_ids = tc.run('get_task')
            continue
        try:
            port = None
            for page_data_id in page_data_ids:
                # step1:Worker:取数-初始化任务
                param = {'store_id': store_id, 'page_data_id': page_data_id, 'port': port, 'job_id': job_id}
                task = TaskController('handle.website.subway.report.SubReportDay', param)
                # 店铺未登录
                if not task.obj.login_flag:
                    # step2:Worker:取数-登录操作
                    login_tc = TaskController('handle.login.tb_login.TaoLogin', task.store)
                    login_tc.run('run')
                    if login_tc.is_success():
                        port = login_tc.port
                        param['port'] = port
                        task = TaskController('handle.website.subway.report.SubReportDay', param)
                    else:
                        Logging.error('param:', param, '登录失败！')
                        raise Exception('param:', param, '登录失败！')
                if not task.is_success():
                    Logging.error('param:', param, '任务初始化失败！')
                    raise Exception('param:', param, '任务初始化失败！')
                try:
                    # step3:Worker:取数-页面操作
                    task.run('operation_page')
                    if not task.is_success():
                        Logging.error('param:', param, '取数-页面操作失败！')
                        raise Exception('param:', param, '取数-页面操作失败！')
                    # step4:Worker:取数-页面文件下载及读取
                    task.run('operation_page_download')
                    if not task.is_success():
                        Logging.error('param:', param, '取数-页面文件下载及读取失败！')
                        raise Exception('param:', param, '取数-页面文件下载及读取失败！')
                    # step5:Worker:取数-数据处理
                    task.run('operation_data_process')
                    if not task.is_success():
                        Logging.error('param:', param, '取数-数据处理失败！')
                        raise Exception('param:', param, '取数-数据处理失败！')
                    # step6:Worker:取数-数据入库
                    task.run('operation_data_input')
                    if not task.is_success():
                        Logging.error('param:', param, '取数-数据入库失败！')
                        raise Exception('param:', param, '取数-数据入库失败！')
                    # step7:Worker:取数-数据备份
                    task.run('operation_data_backup')
                    if not task.is_success():
                        Logging.error('param:', param, '取数-数据备份失败！')
                        raise Exception('param:', param, '取数-数据备份失败！')
                except Exception as e:
                    Logging.error(e)
                    Logging.error('param:', param, ' 页面取数过程失败！')
                tc.run('task_set_end', {'job_id': job_id, 'result': 'success'})
        except Exception as e:
            Logging.error(e)
            Logging.error('job_id:', job_id, ' 任务执行失败！')
            tc.run('task_set_end', {'job_id': job_id, 'result': 'fail'})
        # 继续获取任务
        job_id, store_id, page_data_ids = tc.run('get_task')


if __name__ == '__main__':
    # 全量初始化任务执行
    worker_task_init()
    worker_task_run()
    # 增量初始化任务执行
    worker_task_added()
    worker_task_finish()
    worker_task_run()
