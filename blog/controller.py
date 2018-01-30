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
        self.write({'item': res})


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
        self.write({'item': res})

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


class Category2Handler(web.RequestHandler):
    pass
