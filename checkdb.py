import sqlite3

conn = sqlite3.connect('news.db')
c = conn.cursor()

c.execute("SELECT * FROM news")

a = c.fetchall()
print(len(a))