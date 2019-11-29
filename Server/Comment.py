# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import bcrypt
import pymysql.cursors

app = Flask(__name__)


@app.route('/Comment', methods=['POST'])
def comment():
    comment = request.form["comment"]
    title = "コメント機能"
    return render_template('index.html', title=title)


@app.route('/Login')
def login():
    title = "ログインページ"
    return render_template('login.html', title=title)


@app.route('/Auth', methods=['POST'])
def auth():
    LoginName = request.form["LoginName"]
    LoginPass = request.form["LoginPass"]
    # salt = bcrypt.gensalt()
    # hashed = bcrypt.hashpw(LoginPass.encode(), salt)
    # print(hashed)
    conn = pymysql.connect(
        user='root',
        passwd='root1234',
        host='127.0.0.1',
        port=8889,
        db='PSS'
    )
    c = conn.cursor()
    sql = "SELECT * FROM users WHERE name ={}".format(LoginName)
    c.execute(sql)
    userdata = c.fetchall()[0]
    print(userdata)
    title = "認証"
    return render_template('index.html', title=title)


@app.route('/')
def index():
    title = "コメント機能"
    return render_template('index.html', title=title)


if __name__ == '__main__':
    app.debug = False
    app.run(port=5000, host='0.0.0.0')
