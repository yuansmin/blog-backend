# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
from flask_login import login_required
from flask_login import logout_user
from flask_restful import reqparse

from api import api
from app import json_response
from .user import UserManager


@api.route('/users/login', methods=['POST'])
@json_response
def login():
    args = reqparse.RequestParser().\
        add_argument('email', required=True).\
        add_argument('password', required=True).\
        parse_args()

    return UserManager.login(**args), 200


@api.route('/users/logout', methods=['GET'])
@json_response
def logout():
    logout_user()


@api.route('/users', methods=['GET'])
@login_required
@json_response
def list_users():
    return UserManager.list(), 200


@api.route('/users', methods=['POST'])
@json_response
def create_user_api():
    args = reqparse.RequestParser().\
        add_argument('email', required=True).\
        add_argument('password', required=True).\
        add_argument('name').\
        add_argument('phone_number').\
        add_argument('gender', type=int).\
        add_argument('age', type=int).\
        parse_args()

    return UserManager.create_user(**args), 200


@api.route('/users/password', methods=['POST'])
@login_required
@json_response
def change_password():
    args = reqparse.RequestParser().\
        add_argument('old_password', required=True).\
        add_argument('new_password', required=True).\
        parse_args()

    UserManager.change_cur_user_password_and_logout(**args)

