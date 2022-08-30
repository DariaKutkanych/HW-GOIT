import sqlite3

connection = sqlite3.connect("news.db")

cursor = connection.cursor()
result = cursor.execute('''SELECT * FROM articles''')

for res in result:
    print(res)
