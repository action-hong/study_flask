#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-13 22:36:13
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'


from flask import Flask,render_template
from flask import request
from flask import abort
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html',test='<h1>test</h1>')
	

@app.route('/user/<name>')
def user(name):
	#前面那个name是占位符,在模板中使用
	return render_template('user.html',name=name)



if __name__ == '__main__':
	app.run(debug=True)
	# manager.run()   #使用命令行来决定服务器的启动方式
