# ktis.py

#ktis API
from flask import jsonify
import requests
import re
from module.db import Database
from module.timetable import Timetable
from bs4 import BeautifulSoup as bs

class KTIS:
    #KTIS 로그인
    def Login(json):
        # try:
            with requests.Session() as s:
                login_info = {
                    'txt_user_id': json.get("id"),
                    'txt_passwd': json.get("pw")
                }
                login_req = s.post('https://ktis.kookmin.ac.kr/kmu/com.Login.do?', data=login_info)
                soup = bs(login_req.text, 'html.parser')
                match = soup.find('body', text = re.compile('ktis.kookmin.ac.kr'))
                if match is not None:
                    return "401"

                else:
                    studentid = login_info["txt_user_id"]
                    sql = "SELECT EXISTS (SELECT * FROM users WHERE studentid='"+studentid+"') as success;"
                    exist = Database.GetSQL(sql)
                    #학생이 기존 DB에 있는지 확인
                    if exist[0][0] is 1:
                        return "200"
                    else:
                        post_one = s.get('https://ktis.kookmin.ac.kr/kmu/usb.Usb0102rAGet01.do')
                        soup = bs(post_one.text, 'html.parser')
                        tables = soup.findAll("table")[1]
                        tr = tables.select("tr")[3]
                        tr = tr.select("tr")[2]
                        name = tr.select("td")[1]
                        sql = "INSERT INTO `users` (`studentid`, `name`)  VALUES ('" + studentid + "', '" + name.text + "')"
                        Database.CommitSQL(sql)
                        return "201"

    #DB에 시간표 추가
    def ToDB(json):
        with requests.Session() as s:
            login_info = {
                'txt_user_id': json.get("id"),
                'txt_passwd': json.get("pw")
            }
            login_req = s.post('https://ktis.kookmin.ac.kr/kmu/com.Login.do?', data=login_info)
            soup = bs(login_req.text, 'html.parser')
            match = soup.find('body', text = re.compile('ktis.kookmin.ac.kr'))
            if match is not None:
                return "401"

            else:

                ################################
                ## Login 디버깅용 코드
                ## Users에 사용자 정보가 없으면 추가
                KTIS.Login(json)  
                ################################

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

                studentid = login_info["txt_user_id"]
                sql = "SELECT exist FROM users WHERE studentid = '" + studentid + "'"
                exist = Database.GetSQL(sql)
                #학생의 시간표가 기존 DB에 있는지 확인
                if exist[0][0] is 0: 
                    for item in temp_list:
                        
                        #일반 강의 검색
                        pattern = re.compile(r'[월,화,수,목,금]([A-Z]|\d{1,2})') 
                        match = re.search(pattern, item)
                        time = str(match.group())[1:]
                        Timetable.Add(studentid, item[0], time)

                        #연강 검색
                        pattern = re.compile(r'[,]([A-Z]|\d{1,2})')
                        match = re.search(pattern, item)
                        if match is not None: 
                            time = str(match.group())[1:]
                            Timetable.Add(studentid, item[0], time)
                    return "201"
                else:
                    return "409"
