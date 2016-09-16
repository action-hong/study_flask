#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-13 22:36:13
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

from flask import Flask, render_template, url_for, redirect, session, flash
from flask import request
from flask import abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '407041923@qq.com'
app.config['MAIL_PASSWORD'] = '123123123123123123'  # 密码改了啊,不能传上去哦
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'kkopite<407041923@qq.com>'
app.config['FLASKY_ADMIN'] = 'kkopitehong@gmail.com'  # 会员收件人的
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# 发送地址,主题,模板,参数
def send_mail(to, subject, template, **kw):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    mail.send(msg)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role',
                            lazy='dynamic')  # lazy='dynamic'禁止自动执行查询,user_role.users要加查询函数才会显示数据

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablname__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


def make_shell_context():
    # 注册了app,db等等,直接导入到shell去,省的引用了
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    # 接收到表单的数据,就开始验证传来的数据是否符合要求(NameForm所定义的)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False  # 新客户咯
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
                pass
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        # 重定向,不使用post作为最后的请求方法
        return redirect(url_for('index'))
    return render_template('index.html', name=session.get('name'), form=form, known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    # 前面那个name是占位符,在模板中使用
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    db.create_all()
    manager.run()
# manager.run()   #使用命令行来决定服务器的启动方式
