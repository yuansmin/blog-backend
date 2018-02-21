# -*- coding: utf-8 -*-
import os.path
from datetime import datetime
from hashlib import md5
from PIL import Image

from flask_login import login_user
from sqlalchemy import desc

from app import app
from app import db
from app import APIException
from utils import ensure_dir
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
    def create(cls, **kw):
        user = User(**kw)
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def update(cls, user, **kw):
        """

        :param user: User object
        :param kw: must in [name, phone_number, gender, age]
        :return: User
        """

        params = kw.copy()
        for k in kw:
            if k not in ['name', 'phone_number', 'gender', 'age', 'description',
                         'avatar', 'avatar_large', 'birthday']:
                params.pop(k)

        for k in params:
            setattr(user, k, params[k])
        db.session.commit()
        return user


    @classmethod
    def change_password(cls, user, old_password, new_password):
        user.password = new_password
        db.session.commit()

    @classmethod
    def change_avatar(cls, user, image):
        im = Image.open(image)
        im_hash = md5(im.tobytes() + user.email.encode('ascii')).hexdigest()
        now = datetime.now()
        dirname = os.path.join(app.config['AVATAR_DIR'], str(now.year), str(now.month))
        ensure_dir(dirname)

        def resize_and_save(size, size_name, im_hash):
            avatar = im.resize(size)
            filename = '{0}_{1}.jpg'.format(im_hash, size_name)
            avatar.save(os.path.join(dirname, filename), format='jpeg')

        for size, size_name in [
                    ((73, 73), 'large'),
                    ((48, 48), 'mid'),
                    ((24, 24), 'small')]:
            resize_and_save(size, size_name, im_hash)

        url_base = os.path.join('/static/avatar', str(now.year), str(now.month))
        user.avatar_large = os.path.join(url_base, '{}_large.jpg'.format(im_hash))
        user.avatar_mid = os.path.join(url_base, '{}_mid.jpg'.format(im_hash))
        user.avatar_small = os.path.join(url_base, '{}_small.jpg'.format(im_hash))
        db.session.commit()
        return user
