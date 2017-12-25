import requests
import bs4
import json
import sqlite3
import re
from test import page_scroll_to_bottom


def getSoup(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.text, 'lxml')
    return s

def newsInsert(data):
    conn = sqlite3.connect('news.db')
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
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE url = '%s'" % url)
    check = c.fetchall()
    if(len(check) > 0):
        return True
    else:  
        return False

def ettoday():
    def getList():
        r = page_scroll_to_bottom("https://www.ettoday.net/news/news-list.htm")
        s = bs4.BeautifulSoup(r, 'lxml')
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


applediary()