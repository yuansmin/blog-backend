# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

from blog.models import Base


def init_db():
    engine = create_engine('sqlite:////Users/fancy/work/learn/python/blog/blog.db')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
