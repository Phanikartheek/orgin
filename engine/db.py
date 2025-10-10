import sqlite3

conn = sqlite3.connect("jarvis.db")

cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#query ="INSERT INTO sys_command  VALUES (null, 'one note', 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\ONENOTE.lnk')"
#cursor.execute(query)
#conn.commit()

query ="CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(1000), url VARCHAR(1000))"
cursor.execute(query)

query ="INSERT INTO web_command  VALUES (null, 'Googlephotos', 'https://photos.google.com/')"
cursor.execute(query)
conn.commit()

#testing module
app_name = "one note"
cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
results = cursor.fetchall()
print(results[0][0])