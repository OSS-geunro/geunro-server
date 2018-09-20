# db.py

#RDS MySQL connection module
import pymysql

class Database:
    #DB 설정
    def Config():
        db = pymysql.connect(
            host='ossgeunro.cx4o1leqkzaq.ap-northeast-2.rds.amazonaws.com',
            port=3306,
            user='geunro',
            passwd='E4yjKYaEsny+xxl0b5OejPasRqftJF1R8Y3xjw2j',
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
        result = cursor.fetchone()
        db.close()
        return result

    #DB에 시간표 추가
    def AddTimetable(studentid, day, start, end):
        sql = "UPDATE `users` SET `exist` = '1' WHERE `studentid` = '" + studentid + "';"
        Database.CommitSQL(sql)
        sql = "INSERT INTO `timetable` (`studentid`, `day`, `start`, `end`)  VALUES ('" + studentid + "', '" + day + "', '" + start + "', '" + end + "')"
        Database.CommitSQL(sql)

    #인덱스 재생성
    def ReIndex(dbname):
        sql = "ALTER TABLE " + dbname + " DROP id;"
        Database.CommitSQL(sql)
        sql = "ALTER TABLE " + dbname + " ADD id int primary key auto_increment FIRST;"
        Database.CommitSQL(sql)
