# import pymssql
import pymysql
from DBUtils.PooledDB import PooledDB
import setting
import threading
from common.private_logging import Logging


class DB:
    _instance_lock = threading.Lock()

    def __init__(self):
        self.db_conn = DB.__get_conn()
        self.db_cur = self.db_conn.cursor(cursor=pymysql.cursors.Cursor)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(DB, "_instance"):
            with DB._instance_lock:
                if not hasattr(DB, "_instance"):
                    DB._instance = DB(*args, **kwargs)
        return DB._instance

    @staticmethod
    def __get_conn():
        __pool = PooledDB(creator=pymysql, host=setting.database_data_host, mincached=2, maxcached=20,
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
        Logging.info('db.insert sql:', sql)
        Logging.info('db.insert tuple:', tuple_data)
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
        DB.__pool = None


