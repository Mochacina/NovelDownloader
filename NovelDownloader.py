import os
import sys
from urllib.request import urlopen
import urllib.request
import json
import requests
from bs4 import BeautifulSoup

def switch1(x):
    return {1:"ko", 2:"en", 3:"ja", 4:"zh-CN", 5:"zh-TW", 6:"es", 7:"fr", 8:"vi", 9:"th", 0:"id"}.get(x, "en")

def switch2(x):
    return {1:"ko", 2:"en", 3:"ja", 4:"zh-CN", 5:"zh-TW", 6:"es", 7:"fr", 8:"vi", 9:"th", 0:"id"}.get(x, "ko")

def languPrint(x):
    return {1:"한국어", 2:"영어", 3:"일본어", 4:"중국어 간체", 5:"중국어 번체", 6:"스페인어", 7:"프랑스어", 8:"베트남어", 9:"태국어", 0:"인도네시아어"}.get(x, "비유효값")

def translater(txt, src, des):
    transtxt = urllib.parse.quote(txt)
    data = "source=" + src +"&target=" + des +"&text=" + transtxt
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = json.loads(response.read())
        return response_body['message']['result']['translatedText']
    else:
        return "Error Code:" + rescode

def MainInterface(x):
    if(x==1):
        print("웹소설 번역을 수행합니다.\n")
        FirstInterface()
    elif(x==2):
        print("문장 번역을 수행합니다.\n")
        SecondInterface()
    else:
        print("유효한 값을 입력하여 주시기 바랍니다.\n")

def FirstInterface():
    firstint = 1
    while(firstint>=1):
        siteselect = int(input("번역할 소설 사이트를 선택하십시오.\n1. 픽션프레스(fictionpress.com)\n2. 소설가가 되자(ncode.syosetu.com)\n: "))
        if(siteselect==1):
            sourcelan = "en"
            targetlan = "ko"
            print("픽션프레스(fictionpress.com)에 대한 번역을 수행합니다.\n소설 분류 코드를 입력해 주십시오.")
            nvselect = input(": ")
            html = urlopen('https://www.fictionpress.com/s/' + nvselect)
            soup = BeautifulSoup(html, 'html.parser')
            print(soup.find('b', attrs={'class':'xcontrast_txt'}).text)
            print("작가명: " + soup.find('div', id='profile_top').a.text)
            print('작품소개: \n' + translater(soup.find('div', attrs={'class':'xcontrast_txt'}).text,sourcelan,targetlan))
            numselect = input("번역할 소설의 편수를 선택하세요.\n>>> ")
            html = urlopen('https://www.fictionpress.com/s/' + nvselect + "/" + numselect)
            soup = BeautifulSoup(html, 'html.parser')
            TransData = translater(soup.find('div', id='storytext').text,sourcelan,targetlan)
            print(TransData)
            filename = input("저장할 파일의 이름을 지정해 주십시오.\n>>> ")
            f = open(filename + ".txt", 'w')
            f.write(TransData)
            f.close()
            firstint = 0
        if(siteselect==2):
            sourcelan = "ja"
            targetlan = "ko"
            print("소설가가 되자(ncode.syosetu.com)에 대한 번역을 수행합니다.\n소설 분류 코드를 입력해 주십시오.")
            nvselect = input(": ")
            html = urlopen('http://ncode.syosetu.com/' + nvselect)
            soup = BeautifulSoup(html, 'html.parser')
            print('작품명: \n' + soup.head.title.text)
            print(translater(soup.head.title.text,sourcelan,targetlan))
            print("작가명: " + translater(soup.find('div', attrs={'class': 'novel_writername'}).a.text,sourcelan,targetlan) + "(" + soup.find('div', attrs={'class': 'novel_writername'}).a.text + ")")
            print('작품소개: \n' + translater(soup.find('div', id='novel_ex').text,sourcelan,targetlan))
            numselect = input("번역할 소설의 편수를 선택하세요.\n>>> ")
            html = urlopen('http://ncode.syosetu.com/' + nvselect + "/" + numselect)
            soup = BeautifulSoup(html, 'html.parser')
            TransData = translater(soup.find('div', id='novel_honbun').text,sourcelan,targetlan)
            print(TransData)
            filename = input("저장할 파일의 이름을 지정해 주십시오.\n>>> ")
            f = open(filename + ".txt", 'w')
            f.write(TransData)
            f.close()
            firstint = 0
            
            
            

def SecondInterface():
    secondint = 1
    while(secondint>=1):
        srcselect = int(input("번역할 언어를 선택해 주십시오.\n비유효한 값을 입력시 '영어'로 선택됩니다.\n1.한국어 2.영어 3.일본어 4.중국어 간체 5.중국어 번체\n6.스페인어 7.프랑스어 8.베트남어 9.태국어 0.인도네시아어\n: "))
        sourcelan = switch1(srcselect)
        print(sourcelan)
        print("번역할 언어를 " + languPrint(srcselect) + "로 선택했습니다.")
        dstselect = int(input("번역 결과로 출력할 언어를 선택해 주십시오.\n비유효한 값을 입력시 '한국어'로 선택됩니다.\n1.한국어 2.영어 3.일본어 4.중국어 간체 5.중국어 번체\n6.스페인어 7.프랑스어 8.베트남어 9.태국어 0.인도네시아어\n: "))
        targetlan = switch2(dstselect)
        print(targetlan)
        print("번역 결과로 출력할 언어를 " + languPrint(dstselect) + "로 선택했습니다.")
        secondint = 2
        print("언어를 다시 선택하려면 '8888', 초기 메뉴로 돌아가려면 '9999'를 입력하세요.")
        print("번역 대상 언어: " + languPrint(srcselect) + " / 번역 결과 언어: " + languPrint(dstselect))
        while(secondint>=2):
            TransText = input(">>> ")
            if(TransText == "8888"):
                secondint = 1
            elif(TransText == "9999"):
                secondint = 0
            else:
                TransData = translater(TransText,sourcelan,targetlan)
                print(TransData)
            

client_id = "jyILIHGE11V0S0zdyHyS" # 개발자센터에서 발급받은 Client ID 값
client_secret = "Owdb346w9m" # 개발자센터에서 발급받은 Client Secret 값


TransText = "반갑습니다"
TransData = ""

sourcelan = "en"
targetlan = "ko"

# Main
while 1:
    selecter = int(input("기능을 선택해 주십시오.\n1. 웹소설 번역(fictionpress, syosetu)\n2. 문장 번역\n: "))
    MainInterface(selecter)
