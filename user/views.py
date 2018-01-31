# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
from datetime import datetime

from flask import abort
from flask_restful import reqparse
from flask_login import login_user
from flask_login import login_required
from sqlalchemy import desc

from app import app
from app import db
from app import json_response
from models import User


@app.route('/api/users/login', methods=['POST'])
@json_response
def login():
    args = reqparse.RequestParser().\
        add_argument('email', required=True).\
        add_argument('password', required=True).\
        parse_args()
    user = User.query.filter_by(email=args['email']).one_or_none()
    if not user or not user.check_passowrd(args['password']):
        abort(400, description=u'用户名或密码错误')

    user.last_login = datetime.now()
    db.session.commit()
    # TODO  check if use is active
    result = login_user(user)
    return user.serialize(), 200


@app.route('/api/users', methods=['GET'])
@login_required
@json_response
def list_users():
    users = User.query.order_by(desc("sign_up_time")).all()
    res = {
        'items': [user.serialize() for user in users]
    }
    return res, 200


@app.route('/api/users', methods=['POST'])
@json_response
def signup():
    args = reqparse.RequestParser().\
        add_argument('email', required=True).\
        add_argument('password', required=True).\
        add_argument('name').\
        add_argument('phone_number').\
        parse_args()
    user = User.query.filter_by(email=args['email']).one_or_none()
    if user:
        abort(400, description=u'该邮箱已被注册')

    user = User(**args)
    db.session.add(user)
    db.session.commit()

    return user.serialize(), 200

