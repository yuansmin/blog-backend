# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
from flask_login import current_user
from flask_login import login_required
from flask_login import logout_user
from flask_restful import reqparse

from api import api
from app import json_response
from app import APIException
from .user import UserManager


@api.route('/users/login', methods=['POST'])
@json_response
def login():
    args = reqparse.RequestParser().\
        add_argument('email', required=True).\
        add_argument('password', required=True).\
        parse_args()

    return UserManager.login(**args).serialize(), 200


@api.route('/users/logout', methods=['GET'])
@json_response
def logout():
    logout_user()


@api.route('/users', methods=['GET'])
@login_required
@json_response
def list_users():
    users = UserManager.list()
    res = {
        'items': [user.serialize() for user in users]
    }
    return res, 200


@api.route('/users', methods=['POST'])
@json_response
def create_user_api():
    args = reqparse.RequestParser().\
        add_argument('email', required=True).\
        add_argument('password', required=True).\
        add_argument('name', required=True).\
        add_argument('phone_number').\
        add_argument('description').\
        add_argument('gender', type=int).\
        add_argument('age', type=int).\
        parse_args()

    if UserManager.exists(email=args['email']):
        raise APIException(u'该邮箱已被注册', 400)

    user = UserManager.create(**args)
    return user.serialize(), 201


@api.route('/users/update', methods=['PATCH'])
@login_required
@json_response
def update_user_api():
    args = reqparse.RequestParser().\
        add_argument('phone_number').\
        add_argument('gender', type=int).\
        add_argument('age', type=int).\
        add_argument('description').\
        parse_args()

    user = UserManager.update(current_user, **args)
    return user.serialize(), 200


@api.route('/users/change-password', methods=['POST'])
@login_required
@json_response
def change_password():
    args = reqparse.RequestParser().\
        add_argument('old_password', required=True).\
        add_argument('new_password', required=True).\
        parse_args()

    user = current_user
    if not user.check_passowrd(args['old_password']):
        raise APIException(u'密码错误', 400)

    UserManager.change_password(user=user, **args)
