import sqlite3

connection = sqlite3.connect("quotes.db")

cursor = connection.cursor()
result = cursor.execute('''SELECT q.name as quote, a.name as author, a.birth, a.link, k.name as keyword FROM quotes as q
                           LEFT JOIN authors as a ON a.id = q.author_id
                           LEFT JOIN quote_author_keywords as qt on qt.quote = q.id
                           LEFT JOIN keywords as k ON k.id = qt.keyword
                           LIMIT 50 ''')

for res in result:
    print(res)
