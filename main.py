import xml.etree.ElementTree as ET
import urllib.request
import Func
import gmail
from Func import indent
from urllib.parse import quote

from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import webbrowser
import gmail
import Func
import pickle
import datetime, time
from datetime import *
global tag_list,field_list,value_list
import xml.etree.ElementTree as ET
import smtplib
from  Func import *

from email.mime.text import MIMEText
import spam
strcnt = spam.strlen("test0619");



tag_list, field_list, value_list = [""], [""], [""]

key="04e433744ca6d99a33e8de7d1ca20824"
g_Tk = Tk()
g_Tk.title("Movie")
g_Tk.geometry("400x200+750+200")
photo = PhotoImage(file="movies.png")
imageLabel = Label(g_Tk,image=photo)
imageLabel.pack()

class Mail:
    def __init__(self):
        self.senderAddr, self.recipientAddr = "sb92120@gmail.com", "sb921204@naver.com"
        self.text = ""
    def login(self):
        pass
        self.loginID=gmailID.get()
        self.loginPW = gmailPW.get()
        self.senderAddr = self.loginID + "@gmail.com"
    def write(self):
        self.recipientAddr = gmailRP.get()
        push = False
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
        #print(self.text)

    def send(self):
        msg = MIMEText(self.text, _charset="utf8")
        msg['Subject'] = gmailTitle.get()  # 제목
        msg['From'] = self.senderAddr  # 발신자
        msg['to'] = self.recipientAddr  # 수신자

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.login(self.loginID, self.loginPW)
        s.sendmail(self.senderAddr, self.recipientAddr, msg.as_string())

        s.quit()


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def MovieList(note):
    global tag_list, field_list, value_list
    global title_list, eng_title_list, year_list, director_list, actor_list, nation_list, genre_list
    global temp
    global site_list
    res = 0
    Number=0
    tag_list = ["영화 명", "영화 영문 명", "제작년도", "감독", "출연 배우", "제작 국가", "장르", "관련정보 사이트"]
    title_list = []
    eng_title_list = []
    year_list = []
    director_list = []
    actor_list = []
    nation_list = []
    genre_list = []
    site_list=[]

    field_list = ["title", "eng_title", "year", "director", "actor", "nation", "genre"]
    value_list = [title_list, eng_title_list, year_list, director_list, actor_list, nation_list, genre_list,site_list]

    for element in note.findall("item"):
        RenderText.insert(INSERT, "##영화정보##"+'\n')
        type = 0
        for tag in element.findall("title"):
            for links in tag.findall("link"):
                temp=[]
                temp.append(links.text)
                value_list[7].append(temp)
                RenderText.insert(INSERT, "\n#관련정보 사이트#\n")
                RenderText.insert(INSERT,site_list[Number])
                RenderText.insert(INSERT,'\n\n')

        while type < 7:  # 장르까지 나오도록
            for tag in element.findall(field_list[type]):
                # index = 0
                # while index<len(tag_list):
                if tag.findtext("content") == "":
                    RenderText.insert(INSERT, "정보 없음"+'\n')  # XML파일에 내용 없을시 정보 없음 출력
                    temp = []
                    temp.append('정보없음')
                    value_list[type].append(temp)
                else:
                    RenderText.insert(INSERT, '#'+tag_list[type]+'#\n')
                    temp = []
                    for contents in tag.findall("content"):
                        RenderText.insert(INSERT,contents.text + '\n')
                        temp.append(contents.text)
                    RenderText.insert(INSERT, '\n')
                    value_list[type].append(temp)
                    # index+=1
            type += 1
            res = 1


def InittopText():
    MainText = Label(g_Tk, font='나눔바른펜', text="영화 검색 App",bg="black",fg="white")
    MainText.pack()
    MainText.place(x=150)


def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)

    SearchListBox = Listbox(g_Tk, font='나눔바른펜', activestyle='none', width=15, height=1, borderwidth=12, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set,bg="black",fg="white")
    SearchListBox.insert(1, "     영화목록보기")
    SearchListBox.insert(2, "   사이트바로가기")
    SearchListBox.pack()
    SearchListBox.place(x=120, y=50)


def InitSearchButton():
    SearchButton = Button(g_Tk, font='나눔바른펜', text="  검색  ",command = SearchButtonAction, bg="black",fg="white" )
    SearchButton.pack()
    SearchButton.place(x=170, y=120)


def SearchButtonAction():
    Operation = SearchListBox.curselection()[0]
    if Operation == 0:
        SearchMovie()
    elif Operation == 1:
        ShortCut()

def ShortCut():
    Site_Tk = Tk()
    Site_Tk.geometry("430x150+750+200")
    Site_Tk.title("Movie Site")
    #sphoto = PhotoImage(file="content_blank.png")
    #simageLabe = Label(Site_Tk,image = sphoto)
    #simageLabe.pack()


    SearchText = Label(Site_Tk, font='나눔바른펜', text="[가고 싶은 사이트 검색::](1.CGV/2.메가박스/3.롯데시네마)")
    SearchText.pack()
    SearchText.place(x=10)

    global SiteLabel  # 검색 창
    SiteLabel = Entry(Site_Tk, font='나눔바른펜', width=26, borderwidth=12, relief='ridge')
    SiteLabel.pack()
    SiteLabel.place(x=70, y=55)

    SiteButton = Button(Site_Tk, font='나눔바른펜', text="검색",command= SearchButtonAction6)
    SiteButton.pack()
    SiteButton.place(x=340, y=55)

def SearchButtonAction6():
    sel = SiteLabel.get()
    if (sel == "1"):
        site = 'www.cgv.co.kr'
    elif (sel == "2"):
        site = 'www.megabox.co.kr'
    elif (sel == "3"):
        site = 'www.lottecinema.co.kr'

    webbrowser.open_new(site)



def SearchMovie():
        search_Tk = Tk()
        search_Tk.geometry("410x650+750+100")
        search_Tk.title("Movie Search")


        SearchText = Label(search_Tk, font='나눔바른펜', text="[찾고 싶은 영화 제목 검색]")
        SearchText.pack()
        SearchText.place(x=105)

        global InputLabel #검색 창
        InputLabel = Entry(search_Tk,font='나눔바른펜',width = 26,borderwidth=12,relief='ridge')
        InputLabel.pack()
        InputLabel.place(x=70,y=55)

        #검색 버튼
        SearchButton = Button(search_Tk, font='나눔바른펜', text="검색", command=SearchButtonAction2)
        SearchButton.pack()
        SearchButton.place(x=340, y=57)

        global RenderText
        RenderTextScrollbar = Scrollbar(search_Tk)
        RenderTextScrollbar.pack()
        RenderTextScrollbar.place(x=375, y=200)
        RenderText = Text(search_Tk, width=49, height=25, borderwidth=15, relief='ridge',yscrollcommand=RenderTextScrollbar.set)
        RenderText.place(x=10, y=150)
        RenderTextScrollbar.config(command=RenderText.yview)
        RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
        RenderText.configure(state='normal')


        # 이메일
        tempFont = font.Font(search_Tk,size=12)
        GmailText = Label(search_Tk, font=tempFont, text="[이메일 전송하시겠습니까?(yes/no)]")
        GmailText.pack()
        GmailText.place(y=517,x=10)

        # 이메일 전송 리스트
        global GmailLabel  # 검색 창
        GmailLabel = Entry(search_Tk, font='나눔바른펜', width=3,borderwidth=5, relief='ridge')
        GmailLabel.pack()
        GmailLabel.place(x=285, y=510)


        # XML
        tempFont = font.Font(search_Tk, size=12)
        GmailText = Label(search_Tk, font=tempFont, text="[XML파일로 저장하시겠습니까?(yes/no)]")
        GmailText.pack()
        GmailText.place(y=560, x=10)

        # XML 전송 리스트
        global XMLLabel  # 검색 창
        XMLLabel = Entry(search_Tk, font='나눔바른펜', width=3, borderwidth=5, relief='ridge')
        XMLLabel.pack()
        XMLLabel.place(x=317, y=553)

        # 최종 확인 버튼
        ConfirmButton = Button(search_Tk, font='나눔바른펜', text="      확인      ",command=SearchButtonAction3)
        ConfirmButton.pack()
        ConfirmButton.place(x=150, y=590)

        search_Tk.mainloop()


def SearchButtonAction2():
    RenderText.delete('0.0', END)
    Word = InputLabel.get()
    Oper = "https://apis.daum.net/contents/movie?"  # 목록
    if (len(Word)):
        url = urllib.request.urlopen(Oper + "apikey=" + key + "&q=" + quote("%s" % Word))
    tree = ET.parse(url)
    note = tree.getroot()
    indent(note)
    MovieList(note)

def SearchButtonAction3():
    Word_Gmail = GmailLabel.get()
    Word_XML = XMLLabel.get()

    if ( Word_Gmail == 'yes' and Word_XML == 'yes'):
        global m
        m = Mail()
        gmail_Tk = Tk()
        gmail_Tk.geometry("410x450+750+100")
        gmail_Tk.title("Movie_g_mail&XML")

        # g-mail ID
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTextID = Label(gmail_Tk, font=tempFont, text="[구글ID 입력::]")
        GmailTextID.pack()
        GmailTextID.place(y=50, x=10)

        # g-mail ID 입력 리스트
        global gmailID  # 검색 창
        gmailID = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailID.pack()
        gmailID.place(x=160, y=45)

        # g-mail password
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTextPW = Label(gmail_Tk, font=tempFont, text="[구글 비밀번호 입력::]")
        GmailTextPW.pack()
        GmailTextPW.place(y=100, x=10)

        # g-mail PW 입력 리스트
        global gmailPW  # 검색 창
        gmailPW = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailPW.pack()
        gmailPW.place(x=225, y=95)

        # g-mail Recipient
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTextID = Label(gmail_Tk, font=tempFont, text="[받을 ID 입력::]")
        GmailTextID.pack()
        GmailTextID.place(y=150, x=10)

        # g-mail Recipient 입력 리스트
        global gmailRP  # 검색 창
        gmailRP = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailRP.pack()
        gmailRP.place(x=180, y=145)

        # g-mail title
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTexttitle = Label(gmail_Tk, font=tempFont, text="[메일 제목을 입력::]")
        GmailTexttitle.pack()
        GmailTexttitle.place(y=200, x=10)

        # g-mail title 입력 리스트
        global gmailTitle  # 검색 창
        gmailTitle = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailTitle.pack()
        gmailTitle.place(x=205, y=195)

        # 메일 보내기 버튼
        global  SendButton
        SendButton = Button(gmail_Tk, font='나눔바른펜', text="        보내기        ",command = SearchButtonAction4)
        SendButton.pack()
        SendButton.place(x=135, y=250)


        # XML title
        tempFont = font.Font(gmail_Tk, size=13)
        XMLTextTile = Label(gmail_Tk, font=tempFont, text="[저장 할 XML 제목 입력::]")
        XMLTextTile.pack()
        XMLTextTile.place(y=340, x=10)

        # XML title 입력 리스트
        global XMLTitle  # 검색 창
        XMLTitle = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        XMLTitle.pack()
        XMLTitle.place(x=215, y=335)

        # XML 저장 버튼
        global SaveButton
        SaveButton = Button(gmail_Tk, font='나눔바른펜', text="         저장          ",command = SearchButtonAction5)
        SaveButton.pack()
        SaveButton.place(x=135, y=390)

        gmail_Tk.mainloop()

    elif (Word_Gmail == 'yes' and Word_XML == 'no'):

        m = Mail()
        gmail_Tk = Tk()
        gmail_Tk.geometry("410x350+750+100")
        gmail_Tk.title("Movie_g_mail")

        # g-mail ID
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTextID = Label(gmail_Tk, font=tempFont, text="[구글ID 입력::]")
        GmailTextID.pack()
        GmailTextID.place(y=50, x=10)

        # g-mail ID 입력 리스트
        gmailID = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailID.pack()
        gmailID.place(x=160, y=45)

        # g-mail password
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTextPW = Label(gmail_Tk, font=tempFont, text="[구글 비밀번호 입력::]")
        GmailTextPW.pack()
        GmailTextPW.place(y=100, x=10)

        # g-mail PW 입력 리스트
        gmailPW = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailPW.pack()
        gmailPW.place(x=225, y=95)

        # g-mail Recipient
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTextID = Label(gmail_Tk, font=tempFont, text="[받을 ID 입력::]")
        GmailTextID.pack()
        GmailTextID.place(y=150, x=10)

        # g-mail Recipient 입력 리스트
        gmailRP = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailRP.pack()
        gmailRP.place(x=180, y=145)

        # g-mail title
        tempFont = font.Font(gmail_Tk, size=15)
        GmailTexttitle = Label(gmail_Tk, font=tempFont, text="[메일 제목을 입력::]")
        GmailTexttitle.pack()
        GmailTexttitle.place(y=200, x=10)

        # g-mail title 입력 리스트
        gmailTitle = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        gmailTitle.pack()
        gmailTitle.place(x=205, y=195)

        # 메일 보내기 버튼
        global SendButtonG
        SendButtonG = Button(gmail_Tk, font='나눔바른펜', text="        보내기        ", command=SearchButtonAction7)
        SendButtonG.pack()
        SendButtonG.place(x=135, y=250)


        gmail_Tk.mainloop()

    elif (Word_Gmail == 'no' and Word_XML == 'yes'):
        m = Mail()
        gmail_Tk = Tk()
        gmail_Tk.geometry("380x150+750+100")
        gmail_Tk.title("Movie_XML")

        # XML title
        tempFont = font.Font(gmail_Tk, size=13)
        XMLTextTile = Label(gmail_Tk, font=tempFont, text="[저장 할 XML 제목 입력::]")
        XMLTextTile.pack()
        XMLTextTile.place(y=10, x=10)

        # XML title 입력 리스트
        XMLTitle = Entry(gmail_Tk, font='나눔바른펜', width=15, borderwidth=5, relief='ridge')
        XMLTitle.pack()
        XMLTitle.place(x=10, y=40)

        # XML 저장 버튼
        global SaveButtonX
        SaveButtonX = Button(gmail_Tk, font='나눔바른펜', text="         저장          ", command=SearchButtonAction8)
        SaveButtonX.pack()
        SaveButtonX.place(x=180, y=35)

        gmail_Tk.mainloop()

    elif (Word_Gmail == 'no' and Word_XML == 'no'):
        gmail_Tk = Tk()
        gmail_Tk.geometry("410x150+750+100")
        gmail_Tk.title("result")
        tempFont = font.Font(gmail_Tk, size=13)
        XMLTextTile = Label(gmail_Tk, font=tempFont, text="[이메일 전송X / XML 파일 저장X]\n\n 창을 닫으세요")
        XMLTextTile.pack()
        XMLTextTile.place(y=10, x=10)


def SearchButtonAction4():
    m.login()
    m.write()
    m.add(tag_list, value_list)
    m.send()
    SendButton["text"] = "보내기완료!"


def SearchButtonAction5():
    Word = InputLabel.get()
    Oper = "https://apis.daum.net/contents/movie?"  # 목록
    if (len(Word)):
        url = urllib.request.urlopen(Oper + "apikey=" + key + "&q=" + quote("%s" % Word))
    tree = ET.parse(url)
    note = tree.getroot()

    fileNm = XMLTitle.get()
    ET.ElementTree(note).write("%s.xml" % fileNm)
    SaveButton["text"] = " 저장완료!"

def SearchButtonAction7():
    m.login()
    m.write()
    m.add(tag_list, value_list)
    m.send()
    SendButtonG["text"] = " 보내기완료!\n창을 닫으세요 "


def SearchButtonAction8():
    Word = InputLabel.get()
    Oper = "https://apis.daum.net/contents/movie?"  # 목록
    if (len(Word)):
        url = urllib.request.urlopen(Oper + "apikey=" + key + "&q=" + quote("%s" % Word))
    tree = ET.parse(url)
    note = tree.getroot()

    fileNm = XMLTitle.get()
    ET.ElementTree(note).write("%s.xml" % fileNm)
    SaveButtonX["text"] = "저장완료!\n창을 닫으세요"


InittopText()
InitSearchListBox()
InitSearchButton()



g_Tk.mainloop()


















