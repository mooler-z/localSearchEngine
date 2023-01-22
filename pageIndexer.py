import os
import sys
import sqlite3
import re
from datetime import datetime
from bs4 import BeautifulSoup as bs

passDis = ['exercise', 'tryit']
path = sys.argv[1]

conn = sqlite3.connect('temp.db')
curs = conn.cursor()

"""try:
    curs.execute('DROP TABLE indexes')
except Exception:
    pass

curs.execute('''
    CREATE TABLE indexes (
        ranking int,
        url VARCHAR(100),
        typeOfHeader VARCHAR(3),
        header VARCHAR(143)
    )''')"""

walkPath = os.walk(path)


def filterPages(page):
    sp = os.path.splitext(page)
    if sp[1].lower() == ".html" or sp[1].lower() == ".htm":
        if not sp[0].lower().startswith('exercise') and not re.search('tryit', sp[0].lower()) and not re.search(r'try\d+', sp[0].lower()) and not sp[0].lower().startswith('try') and not re.search(r'playit', sp[0].lower()):
            return True
    else:
        return False


def readFile(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as html:
            return html.read()
    except Exception:
        pass


query = "INSERT INTO indexes values (?, ?, ?, ?)"
count = 0

starts = datetime.now()
for i in walkPath:
    for j in i[2]:
        if filterPages(j):
            fullPath = os.path.join(i[0], j)
            count += 1
            html = readFile(fullPath)
            try:
                BS = bs(html, 'html.parser')
                h1s = BS.find_all('h1')
                h2s = BS.find_all('h2')
            except Exception:
                continue
            for h1 in h1s:
                x = h1.getText()
                if 'Node.js' in x:
                    x.replace('Node.js', 'Nodejs')
                curs.execute(
                    query,
                    [
                        0,
                        "file://"+fullPath,
                        'h1',
                        x
                    ]
                )
            for h2 in h2s:
                x = h2.getText()
                if 'Node.js' in x:
                    x.replace('Node.js', 'Nodejs')
                curs.execute(
                    query,
                    [
                        0,
                        "file://"+fullPath,
                        'h2',
                        x
                    ]
                )


conn.commit()
conn.close()
print("Done in:", datetime.now()-starts, count)
