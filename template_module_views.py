from . import {{ module }}
from {{ appname }}.models import *

from flask import render_template

@{{ module }}.route('/')
def index():
    return render_template("{{ module }}/index.html")
