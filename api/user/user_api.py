# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
from datetime import datetime
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_login import logout_user
from flask_restful import reqparse

from api import api
from app import app
from app import json_response
from app import APIException
from app import admin_required
from utils import check_imgs
from utils import is_before_now
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


@api.route('/users/<int:user_id>', methods=['GET'])
@json_response
def read_user(user_id):
    user = UserManager.get(id=user_id)
    if not user:
        raise APIException(u'用户不存在', 404)
    return user.serialize()


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
        add_argument('phone_number', store_missing=False).\
        add_argument('gender', type=int, store_missing=False).\
        add_argument('birthday', store_missing=False).\
        add_argument('description', store_missing=False).\
        add_argument('name', store_missing=False).\
        parse_args()

    if 'birthday' in args:
        raw_birthday = args['birthday']
        try:
            args['birthday'] = datetime.strptime(
                args['birthday'], '%Y-%m-%d %H:%M:%S')
        except:
            raise APIException(
                'wrong birthday "{}", need "%Y-%m-%d %H:%M:%S"'.format(
                    raw_birthday), 400)
        if not is_before_now(raw_birthday):
            raise APIException(
                'wrong birthday "{}", can not be future'.format(raw_birthday), 400)

    user = UserManager.update(current_user, **args)
    return user.serialize(), 200


@api.route('/users/change-password', methods=['POST'])
@login_required
@json_response
def change_password_api():
    args = reqparse.RequestParser().\
        add_argument('old_password', required=True).\
        add_argument('new_password', required=True).\
        parse_args()

    user = current_user
    if not user.check_passowrd(args['old_password']):
        raise APIException(u'密码错误', 400)

    UserManager.change_password(user=user, **args)


@api.route('/users/change-avatar', methods=['POST'])
@login_required
@json_response
def change_avatar_api():
    files = request.files.keys()
    if not files:
        raise APIException(u'请上传文件', 400)
    image = request.files[files[0]]
    if not check_imgs(image):
        raise APIException(u'非法文件！', 400)
    image.read(app.config['AVATAR_MAX_SIZE'])
    if image.read(5):
        raise APIException(u'文件超过 2M！', 400)
    user = UserManager.change_avatar(current_user, image)
    return user.serialize(), 200
