# -*- coding: utf-8 -*-
from sqlalchemy import desc
from flask_restful import reqparse
from flask_login import current_user
from flask_login import login_required

from api import api
from app import APIException
from app import db
from app import json_response
from .models import Blog
from .models import Category
from .models import Comment
from .models import Label


@api.route('/blogs')
@json_response
def list_blogs():
    blogs = Blog.query.order_by(desc('create_time')).all()
    res = {
        'items': [blog.serialize() for blog in blogs]
    }
    return res, 200


@api.route('/blogs', methods=['POST'])
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


@api.route('/blogs/<int:id>', methods=['GET'])
@json_response
def read_blog(id):
    blog = Blog.query.filter_by(id=id).one_or_none()
    if not blog:
        raise APIException('blog not found', 404)

    return blog.serialize(), 200


@api.route('/blogs/<int:id>', methods=['POST'])
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


@api.route('/blogs/<int:id>', methods=['DELETE'])
@login_required
@json_response
def delete_blog(id):
    Blog.query.filter_by(id=id).delete()
    return


@api.route('/category', methods=['GET'])
@login_required
@json_response
def list_category():
    cgs = Category.query.order_by('index').all()
    res = {
        'items': [cg.serialize() for cg in cgs]
    }
    return res, 200


@api.route('/labels', methods=['GET'])
@login_required
@json_response
def list_labels():
    labels = Label.query.order_by(desc('create_time')).all()
    res = {
        'items': [label.serialize() for label in labels]
    }
    return res, 200


@api.route('/labels', methods=['POST'])
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


@api.route('/labels/<int:id>', methods=['POST'])
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


@api.route('/labels/<int:id>', methods=['DELETE'])
@login_required
@json_response
def delete_label(id):
    Label.query.filter_by(id=id).delete()
    return


@api.route('/comments', methods=['GET'])
@json_response
def list_comments():
    args = reqparse.RequestParser().\
        add_argument('blog_id', type=int, required=True).\
        add_argument('limit', type=int, default=10).\
        add_argument('offset', type=int, default=0).\
        parse_args()
    comments = Comment.query.\
        filter_by(blog_id=args['blog_id']).\
        order_by(desc('create_time')).\
        offset(args['offset']).\
        limit(args['limit']).\
        all()

    res = {
        'items': [c.serialize() for c in comments]
    }
    return res, 200


@api.route('/blogs/<int:id>/comments', methods=['GET'])
@json_response
def list_blog_comments(id):
    args = reqparse.RequestParser().\
        add_argument('limit', type=int, default=10).\
        add_argument('offset', type=int, default=0).\
        parse_args()

    comments = Comment.query.\
        filter_by(blog_id=id).\
        offset(args['offset']).\
        limit(args['limit']).\
        all()
    res = {
        'items': [c.serialize() for c in comments]
    }

    return res, 200


@api.route('/blogs/<int:id>/comments', methods=['POST'])
@login_required
@json_response
def create_comment(id):
    args = reqparse.RequestParser().\
        add_argument('content', required=True).\
        parse_args()
    q = Blog.query.filter_by(id=id)
    res = Blog.query.filter(q.exists()).scalar()
    if not res:
        raise APIException('blog not fount', 404)

    comment = Comment(**args)
    comment.user_id = current_user.id
    comment.blog_id = id
    db.session.add(comment)
    db.session.commit()

    return comment.serialize(), 201


@api.route('/comments/<int:id>', methods=['DELETE'])
@login_required
@json_response
def delete_comment(id):
    Comment.query.filter_by(id=id).delete()
    return

