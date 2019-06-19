from common.db import DataBase

if __name__ == '__main__':
    db1 = DataBase()
    # data1 = db1.query('select * from temp_test')
    # db1.dispose()
    db2 = DataBase()
    db2.dispose()
    print(db1.db_conn, db2.db_conn)
    print(DataBase._DB__pool)