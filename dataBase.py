import sqlite3
from sqlite3 import Error

class DataBase:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
    
    def run_select_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows
    
    def run_insert_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()
