# worktable.py

#worktable control
import time, datetime
from module.db import Database
from module.timetable import Timetable
from datetime import datetime, timedelta
import json

class Worktable:
  #업무 추가
  #(근로시간표이름, 업무이름, 요일, 시작시간, 끝시간, 최소인원)
  def CreateWork(IDs, events, worktable):
    worktable = worktable[0]
    #존재하는 이름인지 확인
    sql = "SELECT name FROM table_list WHERE name = '" + worktable + "'"
    tableName = Database.GetSQL(sql)
    if Database.GetSQL(sql):
      #존재하는경우 409(존재함) 에러 반환
      return "409"
    else:
      # 근무시간표 목록에 추가
      sql = "INSERT INTO `table_list` (`name`)  VALUES ('" + worktable + "')"
      Database.CommitSQL(sql)
      # 근무시간표 ID가져오기 (이름대신 ID사용)
      sql = "SELECT id FROM table_list WHERE name = '" + worktable + "'"
      tableID = Database.GetSQL(sql)[0][0]
      # 업무 목록에 업무 추가
      for i in events:
        sql = "INSERT INTO `work_list` (`worktable`, `name`, `day`, `start`, `end`, `min`)  VALUES ('" + str(tableID) + "', '" + i["name"] + "', '" + i["day"].lower() + "', '" + str(i["start"]) + "', '" + str(i["end"]) + "', '" + i["minimum"] + "')"
        Database.CommitSQL(sql)
      # 근무시간표 사용자 목록에 학번 추가
      for studentid in IDs:
        sql = "INSERT INTO `table_users` (`studentid`, `tablename`)  VALUES ('" + studentid + "', '" + worktable + "')"
        Database.CommitSQL(sql)
      return "201"

  #업무시간 가능한지 확인
  #(요일, 시작, 끝, 최소인원)
  def Available(day, start, end, minimum):
    # s0<=e1 && s1<=e0 then overlap
    time_list = Timetable.GetDay(day)
    student_list = list()
    for block in time_list:
      overlap = False
      for i in time_list[block]:
        if i[0]<=end and start<=i[1]:
          overlap = True 
          break
      if overlap is False:
        student_list.append(block)
      if len(student_list) == minimum:
          break
    return student_list

  #근무시간표 생성
  #(근무시간표이름, 하루최대업무시간, 일주일최대업무시간)
  def Update(worktable, daily, weekly):
    sql = "SELECT studentid FROM users WHERE worktable = '" + worktable + "'"
    days = {"월":timedelta(0),"화":timedelta(0),"수":timedelta(0),"목":timedelta(0),"금":timedelta(0),"timesum":timedelta(0)}
    users = dict((x[0], days) for x in list(Database.GetSQL(sql)))
    sql = "SELECT * FROM work_list WHERE worktable = '" + worktable + "' ORDER BY min DESC"
    works = Database.GetSQL(sql)
    for work in works:
      #0:workid 1:tablename 2:minimum, 3:day, 4:start, 5:end
      student_list = Worktable.Available(work[3], work[4], work[5], work[2])
      for student in student_list:
        if users[student][work[3]] + work[5] - work[4] < daily or users[student]["timesum"] + work[5] - work[4] < weekly:
          users[student][work[3]] += work[5] - work[4]
          users[student]["timesum"] += work[5] - work[4]
          sql = "INSERT INTO `student_list` (`worktable`, `studentid`, `name`, `workid`)  VALUES ('" + worktable + "', '" + str(student) + "', '" + work[1] + "', '" + str(work[0]) + "')"
          Database.CommitSQL(sql)

  def GetList():
    work_list = list()

    sql = "SELECT name FROM table_list"
    data = Database.GetSQL(sql)

    for i in data:
      student_list=list()
      worktable = i[0]
      sql = "SELECT count(table_users.studentid) FROM table_users LEFT OUTER JOIN users ON table_users.studentid = users.studentid WHERE tablename = '" + worktable + "'"
      allcount = Database.GetSQL(sql)[0][0]
      sql = "SELECT count(table_users.studentid) FROM table_users LEFT OUTER JOIN users ON table_users.studentid = users.studentid WHERE exist = 1 and tablename = '" + worktable + "'"
      existcount = Database.GetSQL(sql)[0][0]
      sql = "SELECT table_users.studentid, exist FROM table_users LEFT OUTER JOIN users ON table_users.studentid = users.studentid WHERE tablename = '" + worktable + "'"
      students = Database.GetSQL(sql)
      
      for student in students:
        form = {
          'id' : student[0],
          'exist' : student[1]
        }
        student_list.append(form)

      work = {
        'workName' : worktable,
        'existCount' : existcount,
        'allCount' : allcount,
        'students' : student_list
      }
      work_list.append(work)

    return json.dumps(work_list, ensure_ascii=False)