import xml.etree.ElementTree as ET
import webbrowser
import gmail
import Func
import pickle
import datetime,time
from datetime import *
tag_list, field_list, value_list = [""], [""], [""]



def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def MovieList(note):
    global tag_list, field_list, value_list
    global title_list, eng_title_list, year_list, director_list, actor_list, nation_list, genre_list
    global temp
    res = 0
    tag_list = ["영화 명", "영화 영문 명", "제작년도", "감독", "출연 배우", "제작 국가", "장르"]
    title_list = []
    eng_title_list = []
    year_list = []
    director_list = []
    actor_list = []
    nation_list = []
    genre_list = []

    field_list = ["title", "eng_title", "year", "director", "actor", "nation", "genre"]
    value_list = [title_list, eng_title_list, year_list, director_list, actor_list, nation_list, genre_list]



    for element in note.findall("item"):
        print("\n::::::::::영화정보::::::::::")
        type = 0
        while type < 7:                                             #장르까지 나오도록
            for tag in element.findall(field_list[type]):
                #index = 0
            #while index<len(tag_list):
                if tag.findtext("content") == "":
                    print(tag_list[type], "::","정보없음")       #XML파일에 내용 없을시 정보 없음 출력
                    temp = []
                    temp.append('정보없음')
                    value_list[type].append(temp)
                else:
                    print(tag_list[type])
                    temp = []
                    for contents in tag.findall("content"):
                           print("::",contents.text)
                           temp.append(contents.text)
                    value_list[type].append(temp)
                #index+=1
            type += 1
            res = 1
    if(res == 1):
        answer = input("찾으신 정보를 메일로 보내시겠습니까?(Y/N):: ")
        if answer == "Y" or answer == "y":
            m = gmail.Mail()
            m.login()
            m.write()
            #m.add(Func.tag_list, Func.value_list)
            m.send()

        answer = input("xml파일 저장을 하시겠습니까?(Y/N)::  ")
        if answer == "Y" or answer == "y":
            fileNm = input("저장하실 파일 이름 입력:: ")
            ET.ElementTree(note).write("%s.xml" % fileNm)
    
    if (res==0):
        print("탐색 결과가 없습니다!")

def ConnectCinema():
    print("원하는 극장 홈페이지 선택")
    sel=int(input("1.CGV 2.메가박스 3. 롯데시네마"))
    if(sel==1):
        site='www.cgv.co.kr'
    elif(sel==2):
        site='www.megabox.co.kr'
    elif(sel==3):
        site='www.lottecinema.co.kr'

    webbrowser.open_new(site)








