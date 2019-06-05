import pymysql

class Db:
    def __init__(self,db_type,host,user,passwd,db_name,port=3306,charset='utf-8'):
        self.db_type = db_type
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.port = port
        self.charset = charset

    def db_connect(self):
        if self.db_type.upper() == 'MYSQL':
            db_conn = pymysql.connect(host=self.host,
                                      user=self.user,
                                      database=self.db_name,
                                      password=self.passwd)
            db_cur = db_conn.cursor
        return db_conn, db_cur
