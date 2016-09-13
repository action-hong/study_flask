#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-13 22:36:13
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'


from flask import Flask
from flask import request
from flask import abort
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
	# user_agent = request.headers.get('User-Agent')
	# return '<h1>your browser is %s</h1>' % user_agent

	# response = make_response('<h1>This document carries a cookie!</h1>')
	# response.set_cookie('answer','42')
	# return response
	
	return redirect('http://www.example.com/') #重定向
	
def load_user(id):
	pass


@app.route('/user/<int:id>')
def get_user(id):
	#从数据库获取user,没有就返回404
	user = load_user(id)
	if not user:
		abort(404)
	return '<h1>Hello,%s!</h1>' % name

@app.route('/user/<name>')
def user(name):
	return '<h1>Hello,%s!</h1>' % name



if __name__ == '__main__':
	# app.run()
	manager.run()   #使用命令行来决定服务器的启动方式
