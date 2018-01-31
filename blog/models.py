# -*- coding: utf-8 -*-
from datetime import datetime

from app import db


blog_label = db.Table(
    'blog_label',
    db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id')),
    db.Column('label_id', db.Integer, db.ForeignKey('labels.id'))
    )


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(200))
    content = db.Column('content', db.Text)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)
    published_time = db.Column('published_time', db.DateTime, default=None)
    is_published = db.Column('is_published', db.Boolean, default=False)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    view_count = db.Column('view_count', db.Integer, default=0)
    good_count = db.Column('good_count', db.Integer, default=0)
    labels = db.relationship('Label', secondary=blog_label)

    @staticmethod
    def format_time(time):
        return time.strftime('%Y-%m-%d %H:%M:%S') if time else None

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'create_time': self.format_time(self.create_time),
            'published_time': self.format_time(self.published_time),
            'is_published': self.is_published,
            'category_id': self.category_id,
            'view_count': self.view_count,
            'good_count': self.good_count,
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
            'name': self.name
        }


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200))
    index = db.Column('index', db.Integer)
    create_time = db.Column('create_time', db.DateTime, default=datetime.now)
    user_id = db.Column('user_id', db.Integer)
    blog = db.relationship('Blog', backref='category')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
