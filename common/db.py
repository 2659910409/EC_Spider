import pymssql
import pymysql
from DBUtils.PooledDB import PooledDB
import setting
import threading
from common.private_logging import Logging


class DataBase:
    _instance_lock = threading.Lock()

    def __init__(self):
        cls = pymysql
        self.db_conn = DataBase.__get_conn(cls)
        self.db_cur = self.db_conn.cursor()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(DataBase, "_instance"):
            with DataBase._instance_lock:
                if not hasattr(DataBase, "_instance"):
                    DataBase._instance = DataBase(*args, **kwargs)
        return DataBase._instance

    @staticmethod
    def __get_conn(cls):
        __pool = PooledDB(creator=cls, host=setting.database_data_host, mincached=2, maxcached=20,
                                 port=setting.database_data_port, user=setting.database_data_user,
                                 passwd=setting.database_data_passwd, db=setting.database_data_db_name,
                                 charset=setting.database_data_charset).connection()
        return __pool

    def query(self, sql):
        Logging.info('db.query sql:', sql)
        self.db_cur.execute(sql)
        data = self.db_cur.fetchall()
        return data

    def execute(self, sql):
        Logging.info('db.execute sql:', sql)
        result = self.db_cur.execute(sql)
        self.commit()
        return result

    def insert(self, sql, tuple_data):
        Logging.info('db.insert sql:', sql, tuple_data)
        self.db_cur.execute(sql, tuple_data)
        data = self.query('select last_insert_id() as id')
        key = data[0][0]
        return key

    def delete(self, sql):
        self.db_cur.execute(sql)

    def insert_many(self, sql, data_list):
        Logging.info('db.insert_many sql:', sql, data_list)
        self.db_cur.executemany(sql, data_list)

    def commit(self):
        self.db_conn.commit()

    def close(self):
        self.db_cur.close()
        self.db_conn.close()

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

    def begin(self):
        """
        开启事务
        """
        self.db_conn.autocommit(0)

    def end(self, option='commit'):
        """
        结束事务
        """
        if option == 'commit':
            self.db_conn.commit()
        else:
            self.db_conn.rollback()

    def dispose(self, is_end=1):
        """
        释放连接池资源
        """
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self.db_cur.close()
        self.db_conn.close()


# class DBSystem(DataBase):
#     def __int__(self):
#         self.db_conn = DataBase.__get_conn(pymysql)
#         self.db_cur = self.db_conn.cursor()
#
#
# class DBData(DataBase):
#     # TODO sqlserver 数据库测试
#     def __int__(self):
#         self.db_conn = DataBase.__get_conn(pymssql)
#         self.db_cur = self.db_conn.cursor()


if __name__ == '__main__':
    db = DataBase()
    db.query('select 1;')
    # db = DBSystem()
    # db.query('select 1;')
