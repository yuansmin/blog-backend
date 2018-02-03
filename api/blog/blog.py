# -*- coding: utf-8 -*-
from sqlalchemy import exists
from flask_login import current_user

from .models import Category
from app import APIException
from app import db


class CategoryManager(object):

    @classmethod
    def delete(cls, **kw):
        Category.query.filter_by(**kw).delete()
        db.session.commit()


def create_category(name, index, **kw):
    ret = db.session.query(Category.id).filter_by(name=name).first()
    if ret:
        raise APIException(u'分类 [{0}] 已存在'.format(name), 400)

    cg = Category(
        name=name,
        user_id=current_user.id,
        index=index
    )
    db.session.add(cg)
    db.session.commit()

    return cg.serialize()
