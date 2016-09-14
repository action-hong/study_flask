#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-13 22:36:13
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'


from flask import Flask,render_template,url_for,redirect,session,flash
from flask import request
from flask import abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess'

class NameForm(Form):
	name = StringField('what is your name?',validators=[Required()])		
	submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
	name = None
	form = NameForm()
	#接收到表单的数据,就开始验证传来的数据是否符合要求(NameForm所定义的)
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name != form.name.data:
			flash('looks  you have changed your name!')
		session['name'] = form.name.data
		#重定向,不使用post作为最后的请求方法
		return redirect(url_for('index'))
	return render_template('index.html',name=session.get('name'),form=form)
	

@app.route('/user/<name>')
def user(name):
	#前面那个name是占位符,在模板中使用
	return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500



if __name__ == '__main__':
	app.run(debug=True)
	# manager.run()   #使用命令行来决定服务器的启动方式
