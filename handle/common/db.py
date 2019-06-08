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
