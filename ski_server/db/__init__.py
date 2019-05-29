import os
import pymysql

class DB:

    def __init__(self):
        self.db_conn = self.create_db_connection()
        self.cursor = self.db_conn.cursor()

    def create_db_connection(self):
        db_connection = pymysql.connect(host='192.168.0.123',
                             user=os.getenv("DB_USER","root"),
                             password=os.getenv("DB_PASSWORD","snflRna7890"),
                             db=os.getenv("DB_DBNAME","ski_xray"),
                             cursorclass=pymysql.cursors.DictCursor)
        return db_connection

    def run_query_with_no_return(self,query,args):
        self.cursor.execute(query,args)

    def run_query_with_one_return(self,query,args):
        self.cursor.execute(query,args)
        return self.cursor.fetchone()

    def run_query_with_all_return(self,query,args):
        self.cursor.execute(query,args)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.db_conn.close()
