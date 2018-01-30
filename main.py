# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web

from blog.controller import BlogListHandler
from blog.controller import BlogReadHandler

def make_app():
    return tornado.web.Application([
        (r'/blogs', BlogListHandler),
        (r'/blogs/(\d+)', BlogReadHandler),
    ], debug=True)

if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
