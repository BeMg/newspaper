import sqlite3

conn = sqlite3.connect("news.db")
c = conn.cursor()

c.execute('''CREATE TABLE news
            (
                url text,
                title text,
                main text )''')


# c.execute('''CREATE TABLE news
#             (
#                 date text, 
#                 category text, 
#                 url text,
#                 title text,
#                 main text )''')