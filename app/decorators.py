#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:44:43
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# 有该权限的才能使用该函数
def permission_require(permission):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorator_function

    return decorator


# 只允许admin
def admin_required(f):
    return permission_require(Permission.ADMINISTER)(f)
