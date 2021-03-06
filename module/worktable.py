# worktable.py

#worktable control
import time, datetime
from module.db import Database
from module.timetable import Timetable
from datetime import datetime, timedelta
import json

class Worktable:
  # 업무 추가
  #(근로시간표이름, 업무이름, 요일, 시작시간, 끝시간, 최소인원)
  def CreateWork(events, worktable):
    sql = "SELECT id FROM table_list WHERE name = '" + worktable + "'"
    table_id = str(Database.GetSQL(sql)[0][0])
    # 업무 목록에 업무 추가
    events = json.loads(events)
    for i in events:
      sql = "INSERT INTO `work_list` (`worktable`, `name`, `day`, `start`, `end`, `min`, `tableid`)  VALUES ('" + worktable + "', '" + i["name"] + "', '" + i["day"].lower() + "', '" + str(i["start"]) + "', '" + str(i["end"]) + "', '" + str(i["minimum"]) + "', '" + table_id + "')"
      Database.CommitSQL(sql)
    Worktable.Update(worktable)
    sql = "UPDATE `table_list` SET `exist` = '1' WHERE `name` = '" + worktable + "';"
    Database.CommitSQL(sql)
    return "201"

  # 업무시간 가능한지 확인
  # (최소인원, 요일, 시작, 끝)
  def Available(minimum, day, start, end):
    # s0<=e1 && s1<=e0 then overlap
    # 해당요일의 모든 학생 시간표를 가져옴
    time_list = Timetable.GetDay(day)
    student_list = list()
    # 수업이 업무와 시간이 겹치는지 확인
    for block in time_list:
      overlap = False
      for i in time_list[block]:
        if i[0]<=end and start<=i[1]:
          overlap = True 
          break
      if overlap is False:
        # 겹치는게 없다면 리스트에 해당 수업 추가
        student_list.append(block)
      if len(student_list) == minimum:
          break
    return student_list

  #근무시간표 생성
  #(근무시간표이름, 하루최대업무시간, 일주일최대업무시간)
  def Update(worktable):
    
    sql = "SELECT exist, id FROM table_list WHERE name = '" + worktable + "'"
    exist, table_id = Database.GetSQL(sql)[0]
    if exist is not 1:
      daily = timedelta(hours=5)
      weekly = timedelta(hours=18)
      sql = "SELECT studentid FROM table_users WHERE tablename = '" + worktable + "'"
      days = {"월":timedelta(0),"화":timedelta(0),"수":timedelta(0),"목":timedelta(0),"금":timedelta(0),"timesum":timedelta(0)}
      # 최대근로시간 튜플 생성
      users = dict((x[0], days) for x in list(Database.GetSQL(sql)))
      # 최소 인원 많은 순으로 업무 불러오기
      sql = "SELECT * FROM work_list WHERE worktable = '" + worktable + "' ORDER BY min DESC"
      works = Database.GetSQL(sql)
      for work in works:
        # 0:workid 1:tablename 2:minimum, 3:day, 4:start, 5:end
        # 가능한 학생들을 배열로 저장
        student_list = Worktable.Available(work[2], work[3], work[4], work[5])
        for student in student_list:
          kor = {"mon":"월","tue":"화","wed":"수","thu":"목","fri":"금"}
          day = kor[work[3]]
          # 최대 근로시간 넘기는지 확인
          if users[student][day] + work[5] - work[4] < daily or users[student]["timesum"] + work[5] - work[4] < weekly:
            users[student][day] += work[5] - work[4]
            users[student]["timesum"] += work[5] - work[4]
            sql = "INSERT INTO `student_list` (`worktable`, `studentid`, `name`, `workid`, `worktableid`)  VALUES ('" + worktable + "', '" + str(student) + "', '" + work[1] + "', '" + str(work[0]) + "', '" + str(table_id) + "')"
            Database.CommitSQL(sql)
    
    return str(table_id)

  def GetListStudent(student_id, tablename):
    sql = "SELECT tableid FROM table_users WHERE studentid = '" + student_id + "' AND tablename = '" + tablename + "'"
    data = Database.GetSQL(sql)
    try :
      tableName = data[0][0] 
    except IndexError:
      return 0
    return tableName

  def GetListTeacher(tablename):
    sql = "SELECT exist FROM table_list WHERE name = '" + tablename + "'"
    data = Database.GetSQL(sql)
    try :
      exist = data[0][0] 
    except IndexError:
      return 0
    return exist


  def Access(data):
    worktable = list()
    worktable_name = data['worktable_id']
    sql = "SELECT day, name, start, end, id FROM work_list WHERE worktable = '" + worktable_name + "'"
    worklist = Database.GetSQL(sql)
    days = {'mon':345600, 'tue':432000, 'wed':518400, 'thu':604800, 'fri':691200}
    # 0:요일 1:업무이름 2:시작시간 3:끝시간 4:ID
    for work in worklist:
      student_list = list()
      sql = "SELECT studentid FROM student_list WHERE workid = '" + str(work[4]) + "'"
      students = Database.GetSQL(sql)
      for student in students:
        studentid = {
          'id' : student[0]
        }
        student_list.append(studentid)
      start = (int(work[2].seconds)+days[work[0]])*1000
      end = (int(work[3].seconds)+days[work[0]])*1000
      events = {
        'title': work[1],
        'start': start,
        'end': end,
        'id': work[4],
        'studentid' : student_list
      }
      worktable.append(events)
    return json.dumps(worktable, ensure_ascii=False)

  def DelTable(data):
    worktable = data['worktable']
    sql = "SELECT id FROM table_list WHERE name = '" + worktable + "'"
    worktable_id = str(Database.GetSQL(sql)[0][0])
    sql = "DELETE FROM student_list WHERE worktableid = '" + worktable_id + "'"
    Database.CommitSQL(sql)
    sql = "DELETE FROM table_users WHERE tableid = '" + worktable_id + "'"
    Database.CommitSQL(sql)
    sql = "DELETE FROM work_list WHERE tableid = '" + worktable_id + "'"
    Database.CommitSQL(sql)
    sql = "UPDATE `table_list` SET `exist` = '0' WHERE `name` = '" + worktable + "';"
    Database.CommitSQL(sql)
    return '200'