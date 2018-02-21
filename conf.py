# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
import os.path

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '12345678'
DEBUG = True
AVATAR_MAX_SIZE = 2*1024*1024   # 2M
MAIL_SERVER = 'smtp.exmail.qq.com'
MAIL_PORT = 465
MAIL_USERNAME = 'spider-monitor@thecover.co'
MAIL_PASSWORD = 'Data2016'
MAIL_DEFAULT_SENDER = 'spider-monitor@thecover.co'
MAIL_USE_SSL = True
HOST = 'http://localhost:5000'
CACHE_TYPE = 'simple'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
AVATAR_DIR = os.path.join(STATIC_DIR, 'avatar')