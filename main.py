import requests
import bs4
import json
import sqlite3
import re
from test import page_scroll_to_bottom
import os


def getSoup(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.text, 'lxml')
    return s

def newsInsert(data):
    path = os.path.expanduser("~/newspaper/news.db")
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE url = '%s'" % data[0])
    check = c.fetchall()
    if(len(check) > 0):
        pass
    else:
        c.execute("INSERT INTO news VALUES (?,?,?)", data)
    conn.commit()
    conn.close()

def Checkindb(url):
    path = os.path.expanduser("~/newspaper/news.db")
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE url = '%s'" % url)
    check = c.fetchall()
    if(len(check) > 0):
        return True
    else:  
        return False

def ettoday():
    def getList():
        s = getSoup('https://www.ettoday.net/news/news-list.htm')
        ss = s.find(class_="part_list_2").findAll('a')
        url_list = []
        for i in ss:
            url_list.append("https://www.ettoday.net"+i['href'])
        return url_list
    
    def getContent(url):
        try:
            s = getSoup(url)
            print(url)
            title = s.find(class_=re.compile("title|title_article")).text
            main = ""
            ss = s.find(class_=re.compile("part_area_1|story"))
            sss = ss.findAll('p')
            for i in sss:
                main += i.text
                main += "\n\n"
            print("Success")
            return (url, title, main)
        except:
            print("Fail")
            return None
    
    l = getList()
    
    for i in l:
        if Checkindb(i):
            print("Already have.")
            continue
        else:
            data = getContent(i)
            if data == None:
                pass
            else:
                newsInsert(data)    

def applediary():
    def getList():
        s = getSoup('https://tw.appledaily.com/new/realtime/')
        ss = s.find(class_="rtddd slvl").findAll('a')
        url = []
        for i in ss:
            url.append(i['href'])
        return url
    def getContent(url):
        try:
            print(url)
            s = getSoup(url)
            title = s.find(class_="ndArticle_leftColumn").find('h1').text
            main = s.find(class_="ndArticle_margin").find('p').text
            print("Success")
            return (url, title, main)
        except:
            print("Fail")
            return None

    l = getList()
    
    for i in l:
        if Checkindb(i):
            print("Already have.")
            continue
        else:
            data = getContent(i)
            if data == None:
                pass
            else:
                newsInsert(data)

def udn():
    def getList():
        s = getSoup('https://udn.com/news/breaknews/')
        ss = s.find(id="breaknews_body").find('dl').findAll('h2')
        url = []
        for i in ss:
            url.append('https://udn.com'+i.find('a')['href'])
        return url
    def getContent(url):
        s = getSoup(url)
        try:
            print(url)
            title = s.find(class_='story_art_title').text
            ss = s.find(id='story_body_content').findAll('p')
            main = ""
            for i in ss:
                main += i.text
                main += "\n\n"
            print("Success")
            return (url, title, main)
        except:
            print("Fail")
            return None
    
    l = getList()

    for i in l:
        if Checkindb(i):
            print("Already have.")
            continue
        else:
            data = getContent(i)
            if data == None:
                pass
            else:
                newsInsert(data)

def chinatimes():
    def getList():
        s = getSoup("http://www.chinatimes.com/realtimenews/")
        ss = s.find(class_='listRight').findAll('h2')
        url = []
        for i in ss:
            url.append('http://www.chinatimes.com'+i.find('a')['href'])
        return url
    def getContent(url):
        s = getSoup(url)
        try:
            print(url)
            title = s.find(class_='topich1').find('h1').text
            title = title.replace('\n', '')
            title = title.replace('\r', '')
            title = title.replace(' ', '')
            main = ""
            ss = s.find(class_='arttext marbotm clear-fix').findAll('p')
            for i in ss:
                main += i.text
                main += "\n\n"
            print("Succuss")
            return (url, title, main)
        except:
            print("Fail")
            return None

    l = getList()

    for i in l:
        if Checkindb(i):
            print("Already have.")
            continue
        else:
            data = getContent(i)
            if data == None:
                pass
            else:
                newsInsert(data)


if __name__ == "__main__":
    ettoday()
    applediary()
    udn()
    chinatimes()