from flask import Blueprint

{{ module }} = Blueprint('{{ module }}',
                __name__,
                url_prefix='/{{ module }}',
                template_folder='templates',
                static_folder='static')

from . import views
