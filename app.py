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

def json_response(f):

    @wraps(f)
    def wrapper(*args, **kw):
        res = f(*args, **kw)
        res_code = 200
        res_headers = dict()
        if isinstance(res, dict) or isinstance(res, list):
            res_body = json.dumps(res, indent=4)
        elif isinstance(res, tuple):
            if len(res) == 2:
                res_body, res_code = res
            else:
                res_body, res_code, res_headers = res

            res_body = json.dumps(res_body, indent=4)
        else:
            res_body = res

        return Response(response=res_body, status=res_code,
                        headers=res_headers, mimetype='application/json')

    return wrapper

from blog import views
from user import views
