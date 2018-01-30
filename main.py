# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web

from blog.controller import Blog1Handler
from blog.controller import Blog2Handler
from blog.controller import Category1Handler
from blog.controller import Category2Handler
from blog.controller import Label1Handler
from blog.controller import Label2Handler

def make_app():
    return tornado.web.Application([
        (r'/api/blogs', Blog1Handler),
        (r'/api/blogs/(\d+)', Blog2Handler),
        (r'/api/category', Category1Handler),
        (r'/api/category/(\d+)', Category2Handler),
        (r'/api/labels', Label1Handler),
        (r'/api/labels/(\d+)', Label2Handler),
    ], debug=True)

if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
