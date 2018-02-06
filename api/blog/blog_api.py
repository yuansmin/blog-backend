# -*- coding: utf-8 -*-
from sqlalchemy import desc
from flask_restful import reqparse
from flask_login import current_user
from flask_login import login_required

from api import api
from app import APIException
from app import db
from app import json_response
from .blog import create_blog
from .blog import create_category
from .blog import CategoryManager
from .blog import list_blogs
from .blog import read_blog
from .blog import update_blog
from .models import Blog
from .models import Category
from .models import Comment
from .models import Label


@api.route('/blogs')
@json_response
def list_blogs_api():
    args = reqparse.RequestParser().\
        add_argument('category_id', type=int).\
        add_argument('labels', action='append', default=[]).\
        add_argument('user_id', type=int, default=None).\
        add_argument('keywords', action='append', default=[]).\
        add_argument('offset', type=int, default=0).\
        add_argument('limit', type=int, default=20).\
        parse_args()

    return list_blogs(**args), 200


@api.route('/blogs', methods=['POST'])
@login_required
@json_response
def create_blog_api():
    args = reqparse.RequestParser().\
        add_argument('title').\
        add_argument('content').\
        add_argument('category_id', type=int).\
        parse_args()
    return create_blog(**args), 201


@api.route('/blogs/<int:blog_id>', methods=['GET'])
@json_response
def read_blog_api(blog_id):
    return read_blog(blog_id), 200


@api.route('/blogs/<int:blog_id>', methods=['POST'])
@login_required
@json_response
def update_blog_api(blog_id):
    args = reqparse.RequestParser().\
        add_argument('title', required=False).\
        add_argument('content', required=False).\
        add_argument('category_id', required=False).\
        parse_args()

    return update_blog(blog_id, **args), 200


@api.route('/blogs/<int:blog_id>', methods=['DELETE'])
@login_required
def delete_blog(blog_id):
    Blog.query.filter_by(id=blog_id).delete()
    db.session.commit()


@api.route('/category', methods=['GET'])
@login_required
@json_response
def list_category():
    cgs = Category.query.order_by('index').all()
    res = {
        'items': [cg.serialize() for cg in cgs]
    }
    return res, 200


@api.route('/category', methods=['POST'])
@login_required
@json_response
def create_category_api():
    args = reqparse.RequestParser().\
        add_argument('name', required=True).\
        add_argument('index', default=999).\
        parse_args()

    return create_category(**args), 200


@api.route('/category/<int:category_id>', methods=['DELETE'])
@login_required
@json_response
def delete_category(category_id):
    return CategoryManager.delete(id=category_id), 200


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


@api.route('/labels/<int:label_id>', methods=['POST'])
@login_required
@json_response
def update_label(label_id):
    label = Label.query.filter_by(id=label_id).one_or_none()
    if not label:
        raise APIException('label not found', 404)

    args = reqparse.RequestParser().\
        add_argument('name', required=True).\
        parse_args()
    label.name = args['name']

    db.session.commit()

    return label.serialize(), 200


@api.route('/labels/<int:label_id>', methods=['DELETE'])
@login_required
def delete_label(label_id):
    Label.query.filter_by(id=label_id).delete()
    db.session.commit()


@api.route('/comments', methods=['GET'])
@json_response
def list_comments():
    args = reqparse.RequestParser().\
        add_argument('blog_id', type=int, required=True).\
        add_argument('limit', type=int, default=20).\
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


@api.route('/blogs/<int:comment_id>/comments', methods=['GET'])
@json_response
def list_blog_comments(comment_id):
    args = reqparse.RequestParser().\
        add_argument('limit', type=int, default=10).\
        add_argument('offset', type=int, default=0).\
        parse_args()

    comments = Comment.query.\
        filter_by(blog_id=comment_id).\
        offset(args['offset']).\
        limit(args['limit']).\
        all()
    res = {
        'items': [c.serialize() for c in comments]
    }

    return res, 200


@api.route('/blogs/<int:comment_id>/comments', methods=['POST'])
@login_required
@json_response
def create_comment(comment_id):
    args = reqparse.RequestParser().\
        add_argument('content', required=True).\
        parse_args()
    q = Blog.query.filter_by(id=comment_id)
    res = db.session.query(Blog.id).filter(q.exists()).first()
    if not res:
        raise APIException('blog not fount', 404)

    comment = Comment(**args)
    comment.user_id = current_user.id
    comment.blog_id = id
    db.session.add(comment)
    db.session.commit()

    return comment.serialize(), 201


@api.route('/comments/<int:blog_id>', methods=['DELETE'])
@login_required
def delete_comment(blog_id):
    Comment.query.filter_by(id=blog_id).delete()
    db.session.commit()

