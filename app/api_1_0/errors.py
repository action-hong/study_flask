#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:44:43
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

from flask import jsonify
from app.exceptions import ValidationError
from . import api

def bad_request(message):
    response = jsonify({'error': "bad_request", 'message': message})
    response.status_code = 400
    return response

def unauthorized(message):
    response = jsonify({'error': "unauthorized", 'message': message})
    response.status_code = 401
    return response

def forbidden(message):
    response = jsonify({'error': "forbidden", 'message': message})
    response.status_code = 403
    return response

# 全局处理该异常的程序,其他地方就不需要再做处理了
@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
