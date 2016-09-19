#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-14 16:44:43
# @Author  : kkopite (kkopitehong@gmail.com)
# @Link    : kkopitehong.info
# @Version : 1.0

__author__ = 'kkopite'

import re
import unittest
import threading
from selenium import webdriver
from app import create_app, db
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # pass these test if failed when starting browser
        if cls.client:
            # create exe
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # shutdown logging
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            # create db and add some virtual data
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # add admin
            admin_role = Role.query.filter_by(permission=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # start Flask server in a thread
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop Flask server and Browser
            cls.client.get('http:localhost:5000/shutdown')
            cls.client.close()

            # destroy db
            db.drop_all()
            db.session.commit()

            # delete context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available.')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # home
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        # login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        # login
        self.client.find_element_by_name('email').send_keys('john@exmple.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))

        # profile page
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>joh</h1>' in self.client.page_source)
