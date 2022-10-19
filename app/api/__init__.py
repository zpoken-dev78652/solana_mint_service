from flask import Blueprint

api_bp = Blueprint('api_bp', __name__,
                   template_folder='templates/general',
                   static_folder='../static',
                   static_url_path='assets')

from app.api.routes import *
from app.api.tasks import *
