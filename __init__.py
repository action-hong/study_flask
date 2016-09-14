#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:22:30
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_email import Mail
from flask_momoent import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app()
	mail.init_app()
	moment.init_app()
	db.init_app()

	return app  