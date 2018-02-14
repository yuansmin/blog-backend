# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/31'
"""
import json
from functools import wraps

from flask import Flask
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache

import conf

app = Flask(__name__)
app.config.from_object(conf)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
cache = Cache(app, config={'CACHE_TYPE': app.config['CACHE_TYPE']})

def json_dumps(data, **kw):
    kw.setdefault('ensure_ascii', False)
    return json.dumps(data, **kw)


def json_response(f):

    @wraps(f)
    def wrapper(*args, **kw):
        res = f(*args, **kw)
        res_code = 200
        res_headers = dict()
        if isinstance(res, dict) or isinstance(res, list):
            res_body = json_dumps(res)
        elif isinstance(res, tuple):
            if len(res) == 2:
                res_body, res_code = res
            else:
                res_body, res_code, res_headers = res

            res_body = json_dumps(res_body)
        else:
            res_body = res

        return Response(response=res_body, status=res_code,
                        headers=res_headers, mimetype='application/json')

    return wrapper


def admin_required(f):

    @wraps(f)
    def wrapper(*args, **kw):
        if not current_user.is_admin:
            raise APIException(u'no permission', 403)

        res = f(*args, **kw)
        return res

    return wrapper


class APIException(Exception):

    def __init__(self, message, code=500):
        super(APIException, self).__init__(message)
        self.message = message
        self.code = code


def err_message(msg, code):
    return json_dumps({'message': msg, 'code': code})


@app.errorhandler(APIException)
def error_handler(e):
    return err_message(e.message, e.code), e.code


@app.errorhandler(Exception)
def internal_err_handler(e):
    return err_message(e.message, 500), 500

@app.errorhandler(401)
def unauthorized_handler(e):
    return err_message(u'未登录！请先登录', 401), 401


from api import api

app.register_blueprint(api)
