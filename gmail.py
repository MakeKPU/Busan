global tag_list,field_list,value_list
import xml.etree.ElementTree as ET
import smtplib
from  Func import *

from email.mime.text import MIMEText

class Mail:
    def __init__(self):
        self.senderAddr, self.recipientAddr = "sb92120@gmail.com", "sb921204@naver.com"
        self.text = ""
    def login(self):
        pass
        self.loginID, self.loginPW = input("gmail.com을 제외한 구글ID를 입력하세요:: "), input("비밀번호를 입력하세요:: ")
        self.senderAddr = self.loginID + "@gmail.com"
    def write(self):
        self.recipientAddr = input("받는 사람의 ID를 입력하세요:: ")
        push = True
        s = input("보내실껀가요?(Y/N):: ")
        while (push):
            if s == "Y" or s == "y":
                push = False
                break
            self.text += s + '\n'
    def add(self,tag,value):

        size = len(tag)
        #print(value)

        movies = 0
        for movies in range(len(value[0])):
            i = 0                               #영화명
            for i in range(size):
                if (i == 0):
                    self.text += "--------------------------------\n"
            #self.text += tag[i % size] + " --> " + value[i] + '\n'
                    self.text += tag[i % size] + '\n'
                    for j in value[i][movies]:
                        self.text += " :: " + j + '\n'
                    self.text += "--------------------------------\n"
                else:
                #self.text += tag[i % size] + '\n'
                    self.text += tag[i] + '\n'
                    for j in value[i][movies]:
                        self.text += " :: " + j + '\n'
                i+= 1
            movies += 1
        print(self.text)

    def send(self):
        msg = MIMEText(self.text, _charset="utf8")
        msg['Subject'] = input("메일 제목 입력:: ")  # 제목
        msg['From'] = self.senderAddr  # 발신자
        msg['to'] = self.recipientAddr  # 수신자

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.login(self.loginID, self.loginPW)
        s.sendmail(self.senderAddr, self.recipientAddr, msg.as_string())

        s.quit()


# m=Mail()
# m.login()
# m.write()
# m.send()






