import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import datetime
import random
#import pymysql # ban )))
import sqlite3 # necessary SQLITE 3

#conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql', charset='utf8')
conn = sqlite3.connect('scrap.sqlite') # here name Data Base
cur = conn.cursor()
#cur.execute("USE scraping") # banban

cur.execute('DROP TABLE IF EXISTS use_scraping') # drop table data base

cur.execute('''CREATE TABLE use_scraping
             (title text, content text)''') # so create Data base and columns

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute("INSERT INTO use_scraping (title, content) VALUES (?, ?)", # here VALUES change
        (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urllib.request.urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    store(title, content)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/NY") # here write what you want to start
try:
    while len(links) > 0:
         newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
         print(newArticle)
         links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()
