# -*- coding: utf-8 -*-
import json
from tornado import web

from .models import Blog
from .models import User
from .models import Category
from .models import Label
from .models import Session


class BlogListHandler(web.RequestHandler):

    def get(self):
        session = Session()
        blogs = session.query(Blog).order_by(Blog.id).all()
        res = [blog.serialize() for blog in blogs]
        # import pdb; pdb.set_trace()
        self.write(json.dumps(res, encoding='utf-8'))


class BlogReadHandler(web.RequestHandler):

    def get(self, id):
        session = Session()
        blog = session.query(Blog).filter(Blog.id==id).one()
        self.write(blog.serialize())

