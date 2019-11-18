# -- coding: utf-8 --
# file name : dbModule.py
# pwd : /project_name/app/module/dbModule.py
import pymysql
class Database():
    def __init__(self):
        self.db = pymysql.connect(host='125.131.73.94',
                                  user='root',
                                  password='1234',
                                  port=60041,   # port는 Int
                                  #db='testDB',
                                  db='DB_HILLINGS',
                                  charset='utf8')
        # self.db = pymysql.connect(host='localhost',
        #                           user='root',
        #                           password='1234',
        #                           db='testDB',
        #                           charset='utf8')

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
