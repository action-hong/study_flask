#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:44:43
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class ChangePasswordForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Update Password')

class ResetPasswordRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Update Password')

class ResetPasswordForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('New Password',
                             validators=[Required(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Update Password')

class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters,numbers,dots or underscores')])
    password = PasswordField('password', validators=[Required(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already register')
