# -*- coding: utf-8 -*-
from sqlalchemy import desc
from sqlalchemy import exists
from flask_login import current_user

from .models import Blog
from .models import Category
from app import APIException
from app import db


class BlogManager(object):

    @classmethod
    def create(cls, title, content, category_id, user_id):
        blog = Blog(title=title,
                    content=content,
                    category_id=category_id,
                    user_id=user_id
                    )
        db.session.add(blog)
        db.session.commit()

        return blog

    @classmethod
    def exists(cls, blog_id):
        res = db.session.query(Blog.id).filter_by(id=blog_id).first()
        return bool(res)

    @classmethod
    def increase_view_count(cls, blog_id):
        # TODO: don't query all fields
        blog = Blog.query.filter_by(id=blog_id).first()
        blog.view_count = Blog.view_count + 1
        db.session.commit()


def list_blogs(category_id, labels, user_id, keywords,
               offset, limit):
    # TODO: don't return all fields
    blogs = Blog.query.order_by(desc('create_time')).all()
    res = {
        'items': [blog.serialize() for blog in blogs]
    }
    return res


def read_blog(blog_id):
    if not BlogManager.exists(blog_id):
        raise APIException('blog not fount', 400)
    blog = Blog.query.filter_by(id=blog_id).first()
    BlogManager.increase_view_count(blog_id)

    return blog.serialize()


def create_blog(title, content, category_id):
    blog = BlogManager.create(title, content, category_id,
                       current_user.id)
    return blog.serialize()


def update_blog(blog_id, **kw):
    if not BlogManager.exists(blog_id):
        raise APIException('blog not found', 400)

    blog = Blog.query.filter_by(id=blog_id).first()

    for k in kw:
        setattr(blog, k, kw[k])
    db.session.commit()

    return blog.serialize()


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
