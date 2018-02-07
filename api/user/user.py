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
        return users

    @classmethod
    def login(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_passowrd(password):
            raise APIException(u'用户名或密码错误', 400)

        result = login_user(user)
        user.last_login_time = datetime.now()
        db.session.commit()
        return user

    @classmethod
    def create_user(cls, email, password, name, phone_number,\
                    gender, age):
        user = User(email=email,
                    password=password,
                    name=name,
                    phone_number=phone_number,
                    gender=gender,
                    age=age
                    )

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def change_password(cls, user, old_password, new_password):
        user.password = new_password
        db.session.commit()
