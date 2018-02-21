# -*- coding: utf-8 -*-
import time
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager
from utils import format_time


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), unique=True)
    birthday = db.Column('birthday', db.DateTime, default=None)
    gender = db.Column('gender', db.SmallInteger)   # (0, man) (1, woman)
    email = db.Column('email', db.String(200), unique=True)
    description = db.Column('description', db.String(500))
    avatar_small = db.Column('avatar_small', db.String(200))
    avatar_mid = db.Column('avatar_mid', db.String(200))
    avatar_large = db.Column('avatar_large', db.String(200))
    _password_hash = db.Column('password', db.String(500))
    phone_number = db.Column('phone_number', db.String(50), unique=True)
    sign_up_time = db.Column('sign_up_time', db.DateTime, default=datetime.now)
    last_login_time = db.Column('last_login_time', db.DateTime, default=datetime.now)
    active = db.Column('active', db.Boolean, default=True)
    is_admin = db.Column('is_admin', db.Boolean, default=False)

    @property
    def age(self):
        if not self.birthday:
            return None

        now = datetime.now()
        user_age = now.year - self.birthday.year
        if now.timetuple()[1:] < self.birthday.timetuple()[1:]:
            user_age -= 1
        return user_age

    @property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, value):
        self._password_hash = generate_password_hash(value)

    def check_passowrd(self, password):
        return check_password_hash(self._password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return bool(self.active)

    @property
    def is_anonymous(self):
        return False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'birthday': format_time(self.birthday) if
                            self.birthday else None,
            'gender': self.gender,
            'email': self.email,
            'phone_number': self.phone_number,
            'description': self.description,
            'avatar_small': self.avatar_small,
            'avatar_mid': self.avatar_mid,
            'avatar_large': self.avatar_large,
            'is_admin': self.is_admin,
            'sign_up_time': format_time(self.sign_up_time) if
                            self.sign_up_time else None,
            'last_login_time': format_time(self.last_login_time) if
                            self.last_login_time else None
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).one_or_none()


class UserGroup(db.Model):
    __tabelname__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    scope = db.Column(db.String(255))   # check
    create_time = db.Column(db.DateTime, default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'scope': self.scope,
            'create_time': format_time(self.create_time) if
                                    self.create_time else None,
        }


class GroupManager(db.Model):
    __tablename__ = 'group_user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now)

