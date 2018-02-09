# -*- coding: utf-8 -*-
from flask_restful import reqparse
from flask_login import current_user
from flask_login import login_required

from api import api
from app import APIException
from app import json_response
from .blog import BlogManager
from .blog import CategoryManager
from .blog import CommentManager
from .blog import LabelManager


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

    blogs = BlogManager.list(**args)
    res = {
        'items': [blog.serialize() for blog in blogs]
    }
    return res, 200


@api.route('/blogs', methods=['POST'])
@login_required
@json_response
def create_blog_api():
    args = reqparse.RequestParser().\
        add_argument('title').\
        add_argument('content').\
        add_argument('category_id', type=int).\
        add_argument('labels', action='append', default=[]).\
        parse_args()
    user_id = current_user.id
    labels = args.pop('labels')
    blog = BlogManager.create(user_id=user_id, **args)

    empty_label = []
    for label_id in labels:
        if not LabelManager.exists(id=label_id):
            empty_label.append(label_id)
    if empty_label:
        raise APIException('labels %s not found', empty_label)

    for label_id in labels:
        BlogManager.add_label(blog.id, label_id)
    BlogManager.save()

    return blog.serialize(), 201


@api.route('/blogs/<int:blog_id>', methods=['GET'])
@json_response
def read_blog_api(blog_id):
    return BlogManager.read(blog_id).serialize(), 200


@api.route('/blogs/<int:blog_id>', methods=['POST'])
@login_required
@json_response
def update_blog_api(blog_id):
    args = reqparse.RequestParser().\
        add_argument('title', required=False).\
        add_argument('content', required=False).\
        add_argument('category_id', required=False).\
        parse_args()

    if not BlogManager.exists(blog_id):
        raise APIException('blog %s not found' % blog_id, 404)

    if args.get('category_id') and \
            not CategoryManager.exists(id=args['category_id']):
        raise APIException('category %s not found' % args['category_id'], 404)

    blog = BlogManager.update(blog_id, **args)
    return blog.serialize(), 200


@api.route('/blogs/<int:blog_id>', methods=['DELETE'])
@login_required
@json_response
def delete_blog_api(blog_id):
    BlogManager.delete(blog_id)


@api.route('/category', methods=['GET'])
@login_required
@json_response
def list_category_api():
    cgs = CategoryManager.list()
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

    if CategoryManager.exists(name=args['name']):
        raise APIException(u'分类 [{0}] 已存在'.format(args['name']), 400)

    user_id = current_user.id
    cg = CategoryManager.create(user_id=user_id, **args)
    return cg.serialize(), 201


@api.route('/category/<int:category_id>', methods=['DELETE'])
@login_required
@json_response
def delete_category(category_id):
    if CategoryManager.check_usage(category_id):
        raise APIException('category is being used', 403)
    CategoryManager.delete(id=category_id)


@api.route('/labels', methods=['GET'])
@login_required
@json_response
def list_labels():
    labels = LabelManager.list()
    res = {
        'items': [label.serialize() for label in labels]
    }
    return res, 200


@api.route('/labels', methods=['POST'])
@login_required
@json_response
def create_label_api():
    args = reqparse.RequestParser().\
        add_argument('name', required=True).\
        parse_args()

    label = LabelManager.create(current_user.id, **args)
    return label.serialize(), 201


@api.route('/labels/<int:label_id>', methods=['DELETE'])
@login_required
@json_response
def delete_label(label_id):
    if LabelManager.check_usage(label_id):
        raise APIException('label is being used', 403)
    LabelManager.delete(label_id)


@api.route('/comments', methods=['GET'])
@json_response
def list_comments():
    args = reqparse.RequestParser().\
        add_argument('limit', type=int, default=20).\
        add_argument('offset', type=int, default=0).\
        parse_args()
    comments = CommentManager.list(**args)
    res = {
        'items': [c.serialize() for c in comments]
    }
    return res, 200


@api.route('/blogs/<int:blog_id>/comments', methods=['GET'])
@json_response
def list_blog_comments_api(blog_id):
    args = reqparse.RequestParser().\
        add_argument('limit', type=int, default=10).\
        add_argument('offset', type=int, default=0).\
        parse_args()

    comments = CommentManager.list_blog_comments(blog_id=blog_id, **args)
    res = {
        'items': [c.serialize() for c in comments]
    }
    return res, 200


@api.route('/blogs/<int:blog_id>/comments', methods=['POST'])
@login_required
@json_response
def create_comment_api(blog_id):
    args = reqparse.RequestParser().\
        add_argument('content', required=True).\
        parse_args()
    if not BlogManager.exists(blog_id):
        raise APIException('blog not fount', 404)

    comment = CommentManager.create(
        user_id=current_user.id,
        blog_id=blog_id,
        content=args['content'])
    return comment.serialize(), 201


@api.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
@json_response
def delete_comment_api(comment_id):
    CommentManager.delete(comment_id)

