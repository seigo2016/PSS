# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/Comment', methods=['POST'])
def comment():
    comment = request.form["comment"]
    title = "コメント機能"
    return render_template('index.html', title=title)


@app.route('/')
def index():
    title = "コメント機能"
    return render_template('index.html', title=title)


if __name__ == '__main__':
    app.debug = False
    app.run(port=5000, host='0.0.0.0')
