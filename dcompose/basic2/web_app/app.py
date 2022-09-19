# app.py

import MySQLdb
db_settings = {"host": "web_db", "user": "root", "passwd": "my-password", "db": "db", "charset": "utf8mb4"}
db_conn = MySQLdb.connect(**db_settings) 
cursor = db_conn.cursor()
query = "SELECT * FROM students"
cursor.execute(query)
ret = cursor.fetchall()
print(ret)