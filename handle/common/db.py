# import pymssql
import pymysql
from DBUtils.PooledDB import PooledDB
import setting

# 连接对象
global DATABASE_POOL


class DB:
    def __init__(self):
        self.db_conn = DB.__get_conn()
        self.db_cur = self.db_conn.cursor(cursor=pymysql.cursors.DictCursor)

    @staticmethod
    def __get_conn():
        global DATABASE_POOL
        if DATABASE_POOL is None:
            DATABASE_POOL = PooledDB(creator=pymysql, host=setting.database_data_host, mincached=1, maxcached=20,
                                 port=setting.database_data_port, user=setting.database_data_user,
                                 passwd=setting.database_data_passwd, db=setting.database_data_db_name,
                                 charset=setting.database_data_charset).connection()
        return DATABASE_POOL

    def query(self, sql):
        self.db_cur.execute(sql)
        data = self.db_cur.fetchall()
        return data

    def insert(self, sql, tuple_data):
        self.db_cur.execute(sql, tuple_data)
        data = self.query('select last_insert_id() as id')
        key = data[0]['id']
        return key

    def insert_many(self, sql, data_list):
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
