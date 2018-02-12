# -*- coding: utf-8 -*-
from datetime import datetime

from app import db
from utils import format_time


class BlogLabel(db.Model):
    __tablename__ = 'blog_labels'

    id = db.Column('id', db.Integer, primary_key=True)
    blog_id = db.Column('blog_id', db.Integer, nullable=False)
    label_id = db.Column('label_id', db.Integer, nullable=False)
    create_time = db.Column('create_time', db.Integer, default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'blog_id': self.blog_id,
            'label_id': self.label_id,
            'create_time': format_time(self.create_time) if\
                self.create_time else None
        }


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(200))
    content = db.Column('content', db.Text)
    user_id = db.Column('user_id', db.Integer)
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)
    published_time = db.Column('published_time', db.DateTime, default=None)
    is_published = db.Column('is_published', db.Boolean, default=False)
    labels = db.Column('labels', db.String(200), default='')    # 多个label以 , 隔开
    category_id = db.Column('category_id', db.Integer)
    view_count = db.Column('view_count', db.Integer, default=0)
    good_count = db.Column('good_count', db.Integer, default=0)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'labels': self.labels,
            'user_id': self.user_id,
            'create_time': format_time(self.create_time) if
                self.create_time else None,
            'published_time': format_time(self.published_time) if
                self.published_time else None,
            'is_published': self.is_published,
            'category_id': self.category_id,
            'view_count': self.view_count,
            'good_count': self.good_count,
        }


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column('content', db.String(500))
    user_id = db.Column('user_id', db.Integer)
    blog_id = db.Column('blog_id', db.Integer)
    vote_count = db.Column('good_count', db.Integer, default=0)    # 点赞数, 可加可减
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'use_id': self.user_id,
            'blog_id': self.blog_id,
            'create_time': format_time(self.create_time) if
                self.create_time else None
        }


class Label(db.Model):
    __tablename__ = 'labels'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200))
    user_id = db.Column('user_id', db.Integer)
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'use_id': self.user_id,
            'create_time':format_time(self.create_time) if
                self.create_time else None
        }


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200))
    index = db.Column('index', db.Integer)
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)
    user_id = db.Column('user_id', db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'use_id': self.user_id,
            'create_time': format_time(self.create_time) if
                self.create_time else None
        }

