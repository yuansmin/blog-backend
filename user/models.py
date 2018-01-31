# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200))
    age = db.Column('age', db.Integer)
    gender = db.Column('gender', db.SmallInteger)   # (0, man) (1, woman)
    email = db.Column('email', db.String(200), unique=True)
    _password_hash = db.Column('password', db.String(500))
    phone_number = db.Column('phone_number', db.String(50), unique=True)
    sign_up_time = db.Column('sign_up_time', db.DateTime, default=datetime.now)
    last_login_time = db.Column('last_login_time', db.DateTime, default=datetime.now)
    blog= db.relationship('Blog', backref='user')

    @property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, value):
        self._password_hash = generate_password_hash(value)

    def check_passowrd(self, password):
        return check_password_hash(self._password_hash, password)

    def format_time(self, time):
        return time.strftime('%Y-%m-%d %H:%M:%S') if time else None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone_number': self.phone_number,
            'sign_up_time': self.format_time(self.sign_up_time),
            'last_login_time': self.format_time(self.last_login_time)
        }