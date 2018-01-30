# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, DateTime, \
                    Boolean, ForeignKey, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Table


Engine = create_engine('sqlite:////Users/fancy/work/learn/python/blog/blog.db')
Session = sessionmaker(bind=Engine)


Base = declarative_base()


test = Table(
    'blog_label', Base.metadata,
    Column('blog_id', Integer, ForeignKey('blogs.id')),
    Column('label_id', Integer, ForeignKey('labels.id'))
    )


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(200))
    content = Column('content', Text)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    create_time = Column('create_time', DateTime, default=datetime.now)
    published_time = Column('published_time', DateTime, default=None)
    is_published = Column('is_published', Boolean, default=False)
    category_id = Column('category_id', Integer, ForeignKey('category.id'))
    view_count = Column('view_count', Integer, default=0)
    good_count = Column('good_count', Integer, default=0)
    labels = relationship('Label', secondary=test)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'published_time': self.published_time.strftime('%Y-%m-%d %H:%M:%S') \
                                                    if self.published_time else None,
            'is_published': self.is_published,
            'category_id': self.category_id,
            'view_count': self.view_count,
            'good_count': self.good_count,
        }


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(200))
    age = Column('age', Integer)
    gender = Column('gender', SmallInteger)   # (0, man) (1, woman)
    email = Column('email', String(200))
    password = Column('password', String(500))
    phone_number = Column('phone_number', String(50))
    sign_up_time = Column('sign_up_time', DateTime, default=datetime.now)
    last_login_time = Column('last_login_time', DateTime, default=datetime.now)
    blog= relationship('Blog', backref='user')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
            'sign_up_time': self.sign_up_time,
            'last_login_time': self.last_login_time
        }


class Label(Base):
    __tablename__ = 'labels'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(200))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(200))
    blog = relationship('Blog', backref='category')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
