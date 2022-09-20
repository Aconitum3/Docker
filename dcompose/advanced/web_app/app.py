from flask import Flask
import MySQLdb

app = Flask(__name__)    # アプリケーションのインスタンスを作成

@app.route('/')          # rootページを定義
def root():

    db_settings = {"host": "web_db", "user": "root", "passwd": "my-password", "db": "db", "charset": "utf8mb4"}
    db_conn = MySQLdb.connect(**db_settings) 
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM students")
    ret = cursor.fetchall()
    db_conn.close()

    body = "<table><tr><th>name</th><th>age</th></tr>{}</table>".format(
        "".join([
            "<tr><td>{}</td><td>{}</td>".format(name, age)
            for name, age
            in ret
        ])
        )
    page = "<html><head><title>Students</title></head><body>{body}</body><html>"

    return page.format(body=body)