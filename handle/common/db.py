# import pymssql
import pymysql
from DBUtils.PooledDB import PooledDB
import setting


class DB:
    __pool = None  # 连接对象

    def __init__(self):
        self.db_conn = DB.__get_conn()
        self.db_cur = self.db_conn.cursor(cursor=pymysql.cursors.DictCursor)

    @staticmethod
    def __get_conn():
        if DB.__pool is None:
            DB.__pool = PooledDB(creator=pymysql, host=setting.database_data_host, mincached=1, maxcached=20,
                                 port=setting.database_data_port, user=setting.database_data_user,
                                 passwd=setting.database_data_passwd, db=setting.database_data_db_name,
                                 charset=setting.database_data_charset).connection()
        return DB.__pool

    def query(self, sql):
        self.db_cur.execute(sql)
        data = self.db_cur.fetchall()
        return data

    def insert(self, sql):
        self.db_cur.execute(sql)
        id = int(self.db_cur.insert_id())
        return id

    def insert_many(self, sql, data_list):
        self.db_cur.executemany(sql, data_list)

    def update(self, sql):
        self.db_cur.execute(sql)

    def delete_data(self, table_name, business_date, period):
        self.db_cur.execute("delete from {} where 日期 = {} and 转化周期 = {};".format(table_name, business_date, period))

    def insert_data(self, table_name, field_tuple, num):
        self.db_cur.execute("insert into {} {} values (%s{})".format(table_name, field_tuple, ',%s' * num))

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
