from handle.task import Task
from handle.common.time import sleep
from handle.common.private_logging import Logging


class TaskCreator(Task):

    def task_init(self):
        """初始化任务列表"""
        sql = 'insert into t_job(topic,status,job_params,job_schedule,job_schedule_value,job_sort,created,updated) ' \
              'select ' \
              '\'total\' as topic,0,concat(t1.id,\'|\',GROUP_CONCAT(t2.id, \',\')) as job_params' \
              ',\'realtime\',\'\',2,now(),now() ' \
              'from t_store t1 join t_page_data t2 on 1=1 where t1.status=1 and t2.status=1 group by t1.id;'
        self.db.execute(sql)

    def task_added(self):
        """补入任务列表"""
        sql = 'insert into t_job(topic,status,job_params,job_schedule,job_schedule_value,job_sort,created,updated)' \
              'select ' \
              '\'append\' as topic,0 as status' \
              ',concat(t.store_id,\'|\',GROUP_CONCAT(t.page_data_id, \',\')) as job_params' \
              ',\'realtime\',\'\',1,now(),now() ' \
              'from (' \
              'select distinct t1.id as store_id,t2.id as page_data_id from t_store t1 left join t_page_data t2 on 1=1' \
              'left join t_store_data_log t3 on t1.id = t3.store_id and t2.id = t3.page_data_id ' \
              'where t3.status is null or t3.status != 1 and date(t3.created) = current_date' \
              ') t ' \
              'group by t.store_id;'
        self.db.execute(sql)

    def get_task(self):
        """获取任务"""
        # TODO 数据库事务操作
        sql = 'select id, params from t_job where status = 0 order by job_sort,RAND();'
        jobs = self.db.query(sql)
        if len(jobs) > 0:
            job = jobs[0]
            Logging.info('总任务数：', len(jobs), ' 获取任务：', job)
            job_id = job[0]
            store_id = job[1].split('|')[0]
            page_data_ids = job[1].split('|')[1].split(',')
            return job_id, store_id, page_data_ids
        return None, None, None

    def task_set_start(self, params):
        """任务设置启动"""
        # TODO 事务确认操作，任务可以执行
        sql = 'update t_job set status = 1,start_time=now(),updated=now() where status = 0 and job_id = {}'
        self.db.execute(sql.format(params['job_id']))

    def task_set_end(self, params):
        """任务设置结束"""
        if params['result'] == 'success':
            sql = 'update t_job set status = 2,end_time=now(),updated=now() where status = 1 and job_id = {}'
        else:
            sql = 'update t_job set status = 3,end_time=now(),updated=now() where status = 1 and job_id = {}'
        self.db.execute(sql.format(params['job_id']))

    def task_finish(self):
        """
        任务执行结束检测
        1.等待任务执行结束，任务队列中无任务且没有进行中的任务
        2.执行任务结束后的任务，监控报告发送
        :return:
        """
        while True:
            sql = 'select * from t_job where status in (0,1);'
            jobs = self.db.query(sql)
            # TODO 任务设置超时，强制终止时间机制实现
            finish_flag = True if len(jobs) <= 0 else False
            if finish_flag:
                Logging.info('任务完成')
                # TODO 统一调度入库等操作
                pass
            sleep(30)
