from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from api.blog import blog_api
from api.user import user_api