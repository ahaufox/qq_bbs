# -*- coding: utf-8 -*-
import requests
import time
import sqlite3
from bs4 import BeautifulSoup
import re

def get_cookies(username,password):
    url = 'http://bbs.21ic.com/member.php'
    postData = {'mod': 'logging',
                'action': 'login',
                'loginsubmit': 'yes',
                'infloat': 'yes',
                'lssubmit': 'yes',
                'inajax': 1,
                'username': username,
                'password': password,
                'quickforward': 'yes',
                'handlekey': 'ls'}
    db = sqlite3.connect('db.db')
    sql = """CREATE TABLE "cookies" ("update_time"  INTEGER,"cookies"  TEXT,"username"  TEXT)"""
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
        db.close()
    except:
        pass
    # 解决建表问题和判断表是否存在，不存在数据库，建数据库，不存在表，建表。
    sql = """select * from cookies where username = \"{}\"""".format(username)
    cur = db.cursor()
    cur.execute(sql)
    re=cur.fetchall()
    if re==[]:
        s = requests.session()
        s.post(url, data=postData)
        cookie = s.cookies.get_dict()
        sql = """insert into cookies values ({},\"{}\",\"{}\")""".format(time.time(), cookie, username)
        db = sqlite3.connect('db.db')
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        db.close()
        return cookie
    else:
        if time.time() - re[0][0] > 86400:
            s = requests.session()
            s.post(url, data=postData)
            cookie = s.cookies.get_dict()
            sql = """update cookies set cookies=\"{}\",update_time={} where username=\"{}\"""".format(cookie,time.time(), username)
            db = sqlite3.connect('db.db')
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            db.close()
            return cookie
        else:
            sql = """select cookies from cookies where username = \"{}\"""".format(username)
            db = sqlite3.connect('db.db')
            cur = db.cursor()
            cur.execute(sql)
            re = cur.fetchone()
            return eval(re[0])

username='黄黄'
password='ds1234567890'
cookies={}

cookie=get_cookies(username,password)
res=requests.get('http://bbs.21ic.com/home.php', cookies=cookie).content
res=str(res, encoding='utf-8')

def get_text(text):
    text=re.sub('\n','',text)
    text = re.sub('<[^>]+>', '', text)
    return text
soup = BeautifulSoup(res, "html.parser")
all_a=soup.select('a')
all_href_a=[]
for i in range(0,len(all_a)):
    if all_a[i].get('href')==None:
        pass
    else:
        all_href_a.append(all_a[i].get('href'))
all_href_b=[]
for i in range(0,len(all_href_a)):
    if all_href_a[i][0:30] =='http://bbs.21ic.com/space-uid-':
       all_href_b.append(all_href_a[i])
    else:
        pass

print(all_href_b)
print(len(all_href_b))