# worktable.py

#worktable control
import time, datetime
from module.db import Database
from module.timetable import Timetable
from datetime import datetime, timedelta

class Worktable:

  def CreateWork(worktable, name, day, start, end, minimum):
    sql = "INSERT INTO `work_list` (`worktable`, `name`, `day`, `start`, `end`, `min`)  VALUES ('" + worktable + "', '" + name + "', '" + day + "', '" + str(start) + "', '" + str(end) + "', '" + minimum + "')"
    Database.CommitSQL(sql)

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
