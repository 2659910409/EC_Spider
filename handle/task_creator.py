from handle.task import Task
from handle.common.time import sleep
from common.private_logging import Logging
from random import shuffle


class TaskCreator(Task):

    def task_init(self):
        """初始化任务列表"""
        # TODO 初始化任务时，尚未完成的任务处理 status=0/1 任务处理
        sql = 'insert into t_job(topic,status,job_params,job_schedule,job_schedule_value,job_sort,created,updated) ' \
              'select ' \
              '\'total\' as topic,0,concat(t1.id,\'|\',GROUP_CONCAT(t2.id, \',\')) as job_params' \
              ',\'realtime\',\'\',2,now(),now() ' \
              'from t_store t1 join t_page_data t2 on 1=1 where t1.status=1 and t2.status=1 group by t1.id;'
        self.db.execute(sql)

    def task_added(self):
        """补入任务列表"""
        # TODO 初始化任务时，尚未完成的任务处理 status=0/1 任务处理
        sql = 'insert into t_job(topic,status,job_params,job_schedule,job_schedule_value,job_sort,created,updated) ' \
              'select ' \
              '\'append\' as topic,0 as status' \
              ',concat(t.store_id,\'|\',GROUP_CONCAT(t.page_data_id, \',\')) as job_params' \
              ',\'realtime\',\'\',1,now(),now() ' \
              'from (' \
              'select distinct t1.id as store_id,t2.id as page_data_id from t_store t1 left join t_page_data t2 on 1=1 ' \
              'left join t_store_data_log t3 on t1.id = t3.store_id and t2.id = t3.page_data_id ' \
              'where t3.status is null or t3.status != 1 and date(t3.created) = current_date' \
              ') t ' \
              'group by t.store_id;'
        self.db.execute(sql)

    def get_task(self):
        """获取任务"""
        # TODO 数据库事务操作
        sql = 'select id, job_params from t_job where status = 0 order by job_sort,RAND();'
        jobs = self.db.query(sql)
        if len(jobs) > 0:
            job = jobs[0]
            Logging.info('总任务数：', len(jobs), ' 获取任务：', job)
            job_id = int(job[0])
            store_id = int(job[1].split('|')[0])
            _page_data_ids = job[1].split('|')[1].split(',')
            _page_data_ids.remove('')
            shuffle(_page_data_ids)
            page_data_ids = []
            for s in _page_data_ids:
                page_data_ids.append(int(s))
            return job_id, store_id, page_data_ids
        return None, None, None

    def task_set_start(self, param):
        """任务设置启动"""
        # TODO 事务确认操作，任务可以执行
        sql = 'update t_job set status = 1,start_time=now(),updated=now() where status = 0 and id = {}'
        result = self.db.execute(sql.format(param['job_id']))
        return result

    def task_set_end(self, param):
        """任务设置结束"""
        if param['result'] == 'success':
            sql = 'update t_job set status = 2,end_time=now(),updated=now() where status = 1 and id = {}'
        else:
            sql = 'update t_job set status = 3,end_time=now(),updated=now() where status = 1 and id = {}'
        result = self.db.execute(sql.format(param['job_id']))
        return result

    def task_finish(self):
        """
        任务执行结束检测
        1.等待任务执行结束，任务队列中无任务且没有进行中的任务
        2.执行任务结束后的任务，监控报告发送
        :return:
        """
        while True:
            sql = 'select status, id, topic, job_params from t_job where status in (0,1);'
            jobs = self.db.query(sql)
            # TODO 任务设置超时，强制终止时间机制实现
            finish_flag = True if len(jobs) <= 0 else False
            if finish_flag:
                Logging.info('所有任务执行完成！')
                # TODO 统一调度入库操作
                # TODO 监控告警操作
                pass
            task_waiting = 0
            task_running = 0
            for x in jobs:
                if x[0] == 0:
                    task_waiting = task_waiting + 1
                if x[0] == 1:
                    task_running = task_running + 1
            Logging.info('heartbeat 待执行任务数：', task_waiting, '执行中任务数：', task_running)
            sleep(30)
