import pymssql


class DB:
    def __init__(self, host, user, passwd, db_name, port=3306, charset='utf-8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db_name = db_name
        self.charset = charset
        self.db_conn = None
        self.db_cur = None

    def _create_conn(self):
        self.db_conn = pymssql.connect(server=self.host, port=self.port, user=self.user, password=self.passwd,
                                       database=self.db_name, charset=self.charset)
        self.db_cur = self.db_conn.cursor()

    def query(self, sql):
        self.db_cur.execute(sql)
        data = self.db_cur.fetchall()
        return data

    def insert(self, sql):
        self.db_cur.execute(sql)

    def update(self, sql):
        self.db_cur.execute(sql)

    def delete_data(self, table_name, business_date, period):
        self.db_cur.execute("delete from {} where 日期 = {} and 转化周期 = {};".format(table_name, business_date, period))

    def insert_data(self, table_name, field_tuple, num):
        self.db_cur.execute("insert into {} {} values (%s{})".format(table_name, field_tuple, ',%s' * num))


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
