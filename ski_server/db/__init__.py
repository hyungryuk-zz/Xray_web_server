import os
import pymysql

def create_db_connection() :
    db_connection = pymysql.connect(host='192.168.0.123',
                         user=os.getenv("DB_USER","root"),
                         password=os.getenv("DB_PASSWORD","snflRna7890"),
                         db=os.getenv("DB_DBNAME","ski_xray"),
                         cursorclass=pymysql.cursors.DictCursor)
    return db_connection

