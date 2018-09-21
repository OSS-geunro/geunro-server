# db.py

#RDS MySQL connection module
import pymysql
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

os.environ.get("DB_HOST")
class Database():
    #DB 설정
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

    #SQL Commit 함수
    def CommitSQL(sql):
        db = Database.Config()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()

    #SQL Get 함수
    def GetSQL(sql):
        db = Database.Config()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

class Timetable():
    #DB에 시간표 추가
    def Add(studentid, day, time):
        sql = "UPDATE `users` SET `exist` = '1' WHERE `studentid` = '" + studentid + "';"
        Database.CommitSQL(sql)
        sql = "INSERT INTO `timetable` (`studentid`, `day`, `time`)  VALUES ('" + studentid + "', '" + day + "', '" + time + "')"
        Database.CommitSQL(sql)

    #인덱스 재생성
    def ReIndex(dbname):
        sql = "ALTER TABLE " + dbname + " DROP id;"
        Database.CommitSQL(sql)
        sql = "ALTER TABLE " + dbname + " ADD id int primary key auto_increment FIRST;"
        Database.CommitSQL(sql)
    
    #특정요일의 시간표 가져오기
    def Day(day):
        db = Database.Config()
        cursor = db.cursor()
        sql = "SELECT studentid,start,end FROM timetable JOIN timeblock ON timetable.time = timeblock.time WHERE day ='" + day + "' ORDER BY end"
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        ren = Database.GetSQL(sql) 
        timelist=defaultdict(list)
        for row in ren:
            timelist[row[0]].append(row[1:])
        result=dict(timelist)
        return result