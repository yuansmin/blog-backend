# -*- coding: utf-8 -*-
import json

from sqlalchemy import desc
from flask_restful import reqparse

from app import app
from app import db
from app import json_response
from .models import Blog
from .models import Category
from .models import Label


@app.route('/api/blogs')
@json_response
def list_blogs():
    blogs = Blog.query.order_by(desc('create_time')).all()
    res = {
        'items': [blog.serialize() for blog in blogs]
    }
    return res, 200


@app.route('/api/blogs', methods=['POST'])
@json_response
def create_blog():
    args = reqparse.RequestParser().\
        add_argument('title').\
        add_argument('content').\
        add_category('category_id', type=int).\
        parse_args()
    blog = Blog(**args)
    db.session.add(blog)
    db.session.commit()

    return blog.serialize(), 201


@app.route('/api/blogs/<int:id>', methods=['GET'])
@json_response
def read_blog(id):
    blog = Blog.query.filter_by(id=id).get_or_404()
    return blog.serialize(), 200


@app.route('/api/blogs/<int:id>', methods=['POST'])
@json_response
def update_blog(id):
    blog = Blog.query.filter_by(id=id).first_or_404()
    args = reqparse.RequestParser().\
        add_argument('title', required=False).\
        add_argument('content', required=False).\
        add_argument('category_id', required=False).\
        parse_args()
    if not args:
        return blog.serialize(), 200

    for k in args:
        setattr(blog, k, args[k])
    db.commit()
    return blog.serialize(), 200


@app.route('/api/blogs/<int:id>', methods=['DELETE'])
@json_response
def delete_blog(id):
    Blog.query.filter_by(id=id).delete()
    return


@app.route('/api/category', methods=['GET'])
@json_response
def list_category():
    Category.query.order_by(desc()).all()

