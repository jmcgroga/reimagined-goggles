import os
from flask import Flask

# {{ '{{' }} module_import {{ '}}' }}

app = Flask(__name__)
flask_config = '{{ appname }}.config.Production'

if 'FLASK_CONFIG' in os.environ:
    flask_config = os.environ['FLASK_CONFIG']
app.config.from_object(flask_config)

# {{ '{{' }} module_blueprint {{ '}}' }}
