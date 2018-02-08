# -*- coding: utf-8 -*-
from sqlalchemy import desc

from .models import Blog
from .models import Category
from .models import Comment
from .models import Label
from .models import BlogLabel
from app import APIException
from app import db


class BlogManager(object):
    # TODO: think a better way for manager

    @classmethod
    def save(cls):
        db.session.commit()

    @classmethod
    def create(cls, title, content, category_id, user_id):
        blog = Blog(title=title,
                    content=content,
                    category_id=category_id,
                    user_id=user_id
                    )
        db.session.add(blog)

        return blog

    @classmethod
    def add_label(cls, blog_id, label_id):
        blog_label = BlogLabel(blog_id=blog_id, label_id=label_id)
        db.session.add(blog_label)

    @classmethod
    def exists(cls, blog_id):
        res = db.session.query(Blog.id).filter_by(id=blog_id).first()
        return bool(res)

    @classmethod
    def delete(cls, blog_id):
        Blog.query.filter_by(id=blog_id).delete()

    @classmethod
    def increase_view_count(cls, blog_id):
        # TODO: don't query all fields
        blog = Blog.query.filter_by(id=blog_id).first()
        blog.view_count = Blog.view_count + 1

    @classmethod
    def list(cls, category_id, labels, user_id, keywords,
               offset, limit):
        # TODO: don't return all fields
        # TODO: filter blog by labels & category & keywords
        blogs = Blog.query.order_by(desc('create_time')).\
            offset(offset).\
            limit(limit).\
            all()

        return blogs

    @classmethod
    def read(cls, blog_id):
        if not BlogManager.exists(blog_id):
            raise APIException('blog not fount', 400)
        blog = Blog.query.filter_by(id=blog_id).first()
        # TODO: filter self and admin read
        BlogManager.increase_view_count(blog_id)

        return blog

    @classmethod
    def update(cls, blog_id, **kw):
        if not BlogManager.exists(blog_id):
            raise APIException('blog not found', 400)

        blog = Blog.query.filter_by(id=blog_id).first()

        for k in kw:
            setattr(blog, k, kw[k])
        db.session.commit()

        return blog


class CategoryManager(object):

    @classmethod
    def delete(cls, **kw):
        Category.query.filter_by(**kw).delete()
        db.session.commit()

    @classmethod
    def exists(cls, **kw):
        exists = db.session.query(Category.id).filter_by(**kw).first()
        return bool(exists)

    @classmethod
    def create(cls, name, index, user_id):
        cg = Category(
            name=name,
            user_id=user_id,
            index=index
        )
        db.session.add(cg)
        db.session.commit()

        return cg

    @classmethod
    def list(cls):
        cgs = Category.query.order_by('index').all()
        return cgs

    @classmethod
    def check_usage(cls, category_id):
        """

        :param category_id:
        :return: list [(blog_id,)]
        """
        blogs = db.session.query(Blog.id).filter_by(category_id=category_id).all()
        return blogs


class LabelManager(object):

    @classmethod
    def list(cls):
        labels = Label.query.order_by(desc('create_time')).all()
        return labels

    @classmethod
    def create(cls, user_id, name):
        label = Label(user_id=user_id, name=name)
        db.session.add(label)
        db.session.commit()

        return label

    @classmethod
    def delete(cls, label_id):
        Label.query.filter_by(id=label_id).delete()
        db.session.commit()

    @classmethod
    def exists(cls, **kw):
        exists = db.session.query(Label.id).filter_by(**kw).first()
        return bool(exists)

    @classmethod
    def check_usage(cls, label_id):
        blogs = db.session.query(BlogLabel.blog_id).\
            filter_by(label_id=label_id).all()
        return blogs


class CommentManager(object):

    @classmethod
    def list(cls, limit, offset):
        comments = Comment.query.offset(offset).limit(limit).all()
        return comments

    @classmethod
    def list_blog_comments(cls, blog_id, limit, offset):
        comments = Comment.query. \
            filter_by(blog_id=blog_id). \
            offset(offset). \
            limit(limit). \
            all()

        return comments

    @classmethod
    def create(cls, user_id, blog_id, content):
        comment = Comment(user_id=user_id,
                          blog_id=blog_id,
                          content=content
                          )
        db.session.add(comment)
        db.session.commit()
        return comment

    @classmethod
    def delete(cls, comment_id):
        Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
