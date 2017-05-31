import xml.etree.ElementTree as ET
import urllib.request
import Func
import gmail
from Func import indent
from urllib.parse import quote


key="04e433744ca6d99a33e8de7d1ca20824"


while(1):
    print("""MENU!  1.영화목록보기""")
    Operation=input("input Number:: ")

    if Operation=="2":
        Func.ConnectCinema()
        continue


    if(Operation == "1"):
        Word=str(input("찾고 싶은 영화 제목 입력:: "))
        Oper = "https://apis.daum.net/contents/movie?"  # 목록
        if (len(Word)):
            url = urllib.request.urlopen(Oper + "apikey=" + key + "&q=" + quote("%s" % Word))
        else:
            continue

    tree = ET.parse(url)
    note=tree.getroot()

    indent(note)

    if Operation=="1":
        Func.MovieList(note)
