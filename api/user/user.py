# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy import desc

from app import db
from app import APIException
from .models import User


class UserManager(object):

    @classmethod
    def get(cls, **kw):
        return User.query.filter_by(**kw).first()

    @classmethod
    def exists(cls, **kw):
        return db.session.query(User.id).filter_by(**kw).first()

    @classmethod
    def list(cls):
        users = User.query.order_by(desc('sign_up_time')).all()
        res = {
            'items': [user.serialize() for user in users]
        }
        return res

    @classmethod
    def login(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_passowrd(password):
            raise APIException(u'用户名或密码错误', 400)

        result = login_user(user)
        user.last_login_time = datetime.now()
        db.session.commit()
        return user.serialize()

    @classmethod
    def create_user(cls, email, password, name, phone_number,\
                    gender, age):
        user = User.query.filter_by(email=email).first()
        if user:
            raise APIException(u'该邮箱已被注册', 400)

        user = User(email=email,
                    password=password,
                    name=name,
                    phone_number=phone_number,
                    gender=gender,
                    age=age
                    )

        db.session.add(user)
        db.session.commit()

        return user.serialize()

    @classmethod
    def change_password(cls, user, old_password, new_password):
        if not user.check_passowrd(old_password):
            raise APIException(u'密码错误', 400)

        user.password = new_password
        db.session.commit()

    @classmethod
    def change_cur_user_password_and_logout(cls, old_password,
                                            new_password):
        UserManager.change_password(current_user, old_password,
                                    new_password)
        logout_user()