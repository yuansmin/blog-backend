from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from api.blog import views
from api.user import views