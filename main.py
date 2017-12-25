import requests
import bs4
import json
import sqlite3
import re

def getSoup(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.text, 'lxml')
    return s

def newsInsert(data):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute("INSERT INTO news VALUES (?,?,?)", data)
    conn.commit()
    conn.close()

def ettoday():
    def getList():
        s = getSoup("https://www.ettoday.net/news/news-list.htm")
        ss = s.find(class_="part_list_2").findAll('a')
        url_list = []
        for i in ss:
            url_list.append("https://www.ettoday.net"+i['href'])
        return url_list
    
    def getMain(url):
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
        data = getMain(i)
        if data == None:
            pass
        else:
            newsInsert(data)    

ettoday()