# -*- coding: utf-8 -*-
import json
from tornado import web
from sqlalchemy.orm.exc import NoResultFound

from .models import Blog
from .models import User
from .models import Category
from .models import Label
from .models import Session
from .utils import check_param_completion


class Blog1Handler(web.RequestHandler):
    fields = ['title', 'content', 'category', 'labels']

    def get(self):
        session = Session()
        blogs = session.query(Blog).order_by(Blog.id).all()
        res = [blog.serialize() for blog in blogs]
        self.write({'items': res})


    def post(self):
        body = self.request.body
        data = json.loads(body)
        result = check_param_completion(data, self.fields)
        if result:
            msg = 'missing params %s' % str(result)
            raise web.HTTPError(400, msg)
        blog = Blog(title=data['title'], content=data['content'])
        session = Session()
        session.add(blog)
        session.commit()
        self.set_status(201, 'create blog success')


class Blog2Handler(web.RequestHandler):

    def get(self, id):
        session = Session()
        try:
            blog = session.query(Blog).filter(Blog.id==id).one()
        except NoResultFound:
            raise web.HTTPError(404)

        self.write(blog.serialize())

    def delete(self, id, *args, **kwargs):
        session = Session()
        blog = session.query(Blog).filter(Blog.id==id).one_or_none()
        if not blog:
            return
        session.delete(blog)
        session.commit()
        self.set_status(200, 'delete success')


class Category1Handler(web.RequestHandler):
    fields = ['name']

    def get(self):
        session = Session()
        categories = session.query(Category).all()
        res = [c.serialize() for c in categories]
        self.write({'items': res})

    def post(self):
        data = json.loads(self.request.body)
        result = check_param_completion(data, self.fields)
        if result:
            msg = 'missing params %s' % str(result)
            raise web.HTTPError(400, msg)
        session = Session()
        category = Category(name=data['name'])
        session.add(category)
        session.commit()
        self.set_status(201, 'create category success')
        self.write(category.serialize())


class Category2Handler(web.RequestHandler):
    fields = ['name']

    def get(self, id, *args, **kwargs):
        session = Session()
        try:
            category = session.query(Category).filter(session.id == id).one()
        except NoResultFound:
            raise web.HTTPError(400)

        self.write(category.serialize())

    def delete(self, id):
        session = Session()
        category = session.query(Category).filter(Category.id == id).one_or_none()
        if not category:
            return
        session.delete(category)
        session.commit()
        self.set_status(200, 'delete success')

    def post(self, id, *args, **kwargs):
        session = Session()
        data = json.loads(self.request.body)
        result = check_param_completion(data, self.fields)
        if result:
            msg = 'missing param %s' % str(result)
            raise web.HTTPError(400, msg)
        try:
            category = session.query(Category).filter(Category.id == id).one()
        except NoResultFound:
            raise web.HTTPError(400)

        category.name = data['name']
        session.add(category)
        session.commit()

        self.write(category.serialize())


class Label1Handler(web.RequestHandler):
    fields = ['name']

    def get(self, *args, **kwargs):
        session = Session()
        labels = session.query(Label).all()
        res = {
            'items': [label.serialize() for label in labels]
        }
        self.write(res)

    def post(self):
        data = json.loads(self.request.body)
        result = check_param_completion(data, self.fields)
        if result:
            msg = 'missing param %s' % str(result)
            raise web.HTTPError(400, msg)

        label = Label(name=data['name'])
        session = Session()
        session.add(label)
        session.commit()

        self.write(label.serialize())


class Label2Handler(web.RequestHandler):

    fields = ['name']

    def get(self, id):
        session = Session()
        try:
            label = session.query(Label).filter(Label.id == id).one()
        except NoResultFound:
            raise web.HTTPError(400)

        self.write(label.serialize())

    def delete(self, id):
        session = Session()
        label = session.query(Label).filter(Label.id == id).one_or_none()
        if not label:
            return
        session.delete(label)
        session.commit()
        self.set_status(200, 'delete success')

    def post(self, id, *args, **kwargs):
        session = Session()
        data = json.loads(self.request.body)
        result = check_param_completion(data, self.fields)
        if result:
            msg = 'missing param %s' % str(result)
            raise web.HTTPError(400, msg)
        try:
            label = session.query(Label).filter(Label.id == id).one()
        except NoResultFound:
            raise web.HTTPError(400)

        label.name = data['name']
        session.add(label)
        session.commit()

        self.write(label.serialize())
