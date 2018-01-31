# -*- coding: utf-8 -*-
import json

from sqlalchemy import desc
from flask_restful import reqparse
from flask_login import current_user
from flask_login import login_required

from app import app
from app import APIException
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
@login_required
@json_response
def create_blog():
    args = reqparse.RequestParser().\
        add_argument('title').\
        add_argument('content').\
        add_argument('category_id', type=int).\
        parse_args()
    blog = Blog(**args)
    blog.user_id = current_user.id
    db.session.add(blog)
    db.session.commit()

    return blog.serialize(), 201


@app.route('/api/blogs/<int:id>', methods=['GET'])
@json_response
def read_blog(id):
    blog = Blog.query.filter_by(id=id).one_or_none()
    if not blog:
        raise APIException('blog not found', 404)

    return blog.serialize(), 200


@app.route('/api/blogs/<int:id>', methods=['POST'])
@login_required
@json_response
def update_blog(id):
    blog = Blog.query.filter_by(id=id).one_or_none()
    if not blog:
        raise APIException('blog not found', 404)

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
@login_required
@json_response
def delete_blog(id):
    Blog.query.filter_by(id=id).delete()
    return


@app.route('/api/category', methods=['GET'])
@login_required
@json_response
def list_category():
    cgs = Category.query.order_by(desc()).all()
    res = {
        'items': [cg.serialize() for cg in cgs]
    }
    return res, 200


@app.route('/api/labels', methods=['GET'])
@login_required
@json_response
def list_labels():
    labels = Label.query.order_by(desc('create_time')).all()
    res = {
        'items': [label.serialize() for label in labels]
    }
    return res, 200


@app.route('/api/labels', methods=['POST'])
@login_required
@json_response
def create_label():
    args = reqparse.RequestParser().\
        add_argument('name', required=True).\
        parse_args()
    label = Label(**args)
    label.user_id = current_user.id
    db.session.add(label)
    db.session.commit()

    return label.serialize(), 201


@app.route('/api/labels/<int:id>', methods=['POST'])
@login_required
@json_response
def update_label(id):
    label = Label.query.filter_by(id=id).one_or_none()
    if not label:
        raise APIException('label not found', 404)

    args = reqparse.RequestParser().\
        add_argument('name', required=True).\
        parse_args()
    label.name = args['name']

    db.session.commit()

    return label.serialize(), 200


@app.route('/api/labels/<int:id>', methods=['DELETE'])
@login_required
@json_response
def delete_label(id):
    Label.query.filter_by(id=id).delete()
    return
