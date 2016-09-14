#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:38:10
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

from flask import Blueprint

main = Blueprint('main',__name__)

from . import views,errors
