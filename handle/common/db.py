import pymssql


class DB:
    def __init__(self, host, user, passwd, db_name, port=3306, charset='utf-8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db_name = db_name
        self.charset = charset

    def create_conn(self):
        db_conn = pymssql.connect(server=self.host, port=self.port, user=self.user, password=self.passwd,
                                  database=self.db_name, charset=self.charset)
        db_cur = db_conn.cursor()
        return db_conn, db_cur

    def get_work_info(self, work_name):
        """
        根据接收的任务名查找任务详细
        :param work_name: 任务名称
        :return:
        """
        db_conn, db_dur = self.create_conn()
        work_info_sql = "select * from t_task where work_name = {}".format(work_name)
        db_dur.execute(work_info_sql)
        work_info = db_dur.fetchall()
        return work_info





    def input(self, data):
        """
        delete data business primary key
        insert data
        :param data:
        :return: True/False
        """
        pass

    def input_batch(self, datas):
        """"""
        pass
