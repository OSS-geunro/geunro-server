# db.py

#RDS MySQL connection module
import pymysql
import os
from dotenv import load_dotenv, find_dotenv
from collections import defaultdict

load_dotenv(find_dotenv())

os.environ.get("DB_HOST")
class Database:
    #DB 설정
    #.env 참조
    def Config():
        db = pymysql.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            passwd=os.environ.get("DB_PASSWD"),
            db='oss', 
            charset='utf8'
        )
        return db

    #SQL Commit
    def CommitSQL(sql):
        db = Database.Config()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()

    #SQL Get
    def GetSQL(sql):
        db = Database.Config()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    #인덱스 재생성
    def ReIndex(dbname):
        sql = "ALTER TABLE " + dbname + " DROP id;"
        Database.CommitSQL(sql)
        sql = "ALTER TABLE " + dbname + " ADD id int primary key auto_increment FIRST;"
        Database.CommitSQL(sql)



