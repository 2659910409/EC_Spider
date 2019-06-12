import pymssql
import setting


class DB:
    def __init__(self):
        self.host = setting.database_data_host
        self.user = setting.database_system_user
        self.passwd = setting.database_system_passwd
        self.port = setting.database_system_port
        self.db_name = setting.database_system_db_name
        self.charset = setting.database_system_charset
        self.db_conn = None
        self.db_cur = None
        self._create_conn()

    def _create_conn(self):
        self.db_conn = pymssql.connect(server=self.host, port=self.port, user=self.user, password=self.passwd,
                                       database=self.db_name, charset=self.charset)
        self.db_cur = self.db_conn.cursor()

    def query_fetchall(self, sql):
        self.db_cur.execute(sql)
        data = self.db_cur.fetchall()
        return data

    def query_fetchone(self, sql):
        self.db_cur.execute(sql)
        data = self.db_cur.fetchone()
        return data

    def insert(self, sql):
        self.db_cur.execute(sql)

    def insert_many(self, sql, data_list):
        self.db_cur.executemany(sql, data_list)

    def update(self, sql):
        self.db_cur.execute(sql)

    def commit(self):
        self.db_conn.commit()

    def close(self):
        self.db_cur.close()
        self.db_conn.close()

