from common.db import DB

if __name__ == '__main__':
    db1 = DB()
    # data1 = db1.query('select * from temp_test')
    # db1.dispose()
    db2 = DB()
    db2.dispose()
    print(db1.db_conn, db2.db_conn)
    print(DB._DB__pool)