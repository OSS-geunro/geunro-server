# timetable.py

#timetable control
import pymysql
import os
from db import Database
from dotenv import load_dotenv, find_dotenv
from collections import defaultdict

class Timetable:
    #DB에 시간표 추가
    def Add(studentid, day, time):
        sql = "UPDATE `users` SET `exist` = '1' WHERE `studentid` = '" + studentid + "';"
        Database.CommitSQL(sql)
        sql = "INSERT INTO `timetable` (`studentid`, `day`, `time`)  VALUES ('" + studentid + "', '" + day + "', '" + time + "')"
        Database.CommitSQL(sql)
    
    #특정요일의 시간표 가져오기
    def GetDay(day):
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
