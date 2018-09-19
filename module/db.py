# db.py

#RDS MySQL connection module
import pymysql

class Database:

    def CommitSQL(sql):
        db = pymysql.connect(
            host='ossgeunro.cx4o1leqkzaq.ap-northeast-2.rds.amazonaws.com', 
            port=3306, 
            user='', 
            passwd='', 
            db='oss', 
            charset='utf8'
        )
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()

    def AddTimetable(studentid, day, start, end):
        sql = "INSERT INTO `timetable` (`studentid`, `day`, `start`, `end`)  VALUES ('" + studentid + "', '" + day + "', '" + start + "', '" + end + "')"
        Database.CommitSQL(sql)

    def ReIndex(dbname):
        sql = "ALTER TABLE " + dbname + " DROP id;"
        Database.CommitSQL(sql)
        sql = "ALTER TABLE " + dbname + " ADD id int primary key auto_increment FIRST;"
        Database.CommitSQL(sql)
