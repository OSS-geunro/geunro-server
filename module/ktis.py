# ktis.py

#ktis timetable parser
from flask import jsonify
import requests
import re
import dis
from module.db import Database
from bs4 import BeautifulSoup as bs

#시작시간 
start_time = {
        "1":"9:00", "A":"9:00",
        "2":"10:00", "B":"10:30",
        "3":"11:00", "C":"12:00",
        "4":"12:00", "D":"13:30",
        "5":"13:00", "E":"15:00",
        "6":"14:00", "F":"16:30",
        "7":"15:00", "G":"18:00",
        "8":"16:00", "H":"19:25",
        "9":"17:00", "I":"20:50",
        "10":"18:00",
        "11":"18:55",
        "12":"19:50",
        "13":"20:45",
        "14":"21:40",
}

end_time = {
        "1":"09:50", "A":"10:15",
        "2":"10:50", "B":"11:45",
        "3":"11:50", "C":"13:15",
        "4":"12:50", "D":"14:45",
        "5":"13:50", "E":"16:15",
        "6":"14:50", "F":"17:45",
        "7":"15:50", "G":"19:15",
        "8":"16:50", "H":"20:40",
        "9":"17:50", "I":"22:05",
        "10":"18,50",
        "11":"19:45",
        "12":"20:40",
        "13":"21:15",
        "14":"22:10",
}

# Session 생성, with 구문 안에서 유지
def GetTimetable(json):
    with requests.Session() as s:
        login_info = {
            'txt_user_id': json.get("id"),
            'txt_passwd': json.get("pw")
        }
        
        login_req = s.post('http://ktis.kookmin.ac.kr/kmu/com.Login.do?', data=login_info)
        
        # 로그인체크
        if login_req.status_code != 200:
            raise Exception('Login Error')

        # 로그인 세션 유지
        
        # 수강신청내역 불러오기
        post_one = s.get('https://ktis.kookmin.ac.kr/kmu/usb.Usb0102rAGet01.do')
        soup = bs(post_one.text, 'html.parser')

        #시간표 분리
        tables = soup.findAll("table")[1]
        tr_list = tables.select("tr")[8:]
        temp_list = list()
        for tr in tr_list:
            td = tr.select("td")[6]
            string = td.text.replace(", ", ",").replace("7호관", "칠호관")
            temp_list += string.split()

        days = {
            "월":"mon",
            "화":"tue",
            "수":"wed",
            "목":"thu",
            "금":"fri"
        }

        studentid = login_info["txt_user_id"]
        for item in temp_list:
            
            #일반 강의 검색
            pattern = re.compile(r'[월,화,수,목,금]([A-Z]|\d{1,2})') 
            match = re.search(pattern, item)
            time = str(match.group())[1:]
            Database.AddTimetable(studentid, days[item[0]], start_time[time],end_time[time])

            #연강 검색
            pattern = re.compile(r'[,]([A-Z]|\d{1,2})')
            match = re.search(pattern, item)
            if match is not None: 
                time = str(match.group())[1:]
                Database.AddTimetable(studentid, days[item[0]], start_time[time],end_time[time])
        return "SQL commit success"
        
    #TODO: 수업 시작, 종료시간 DB화