import os
from {{ appname }} import app

if 'FLASK_CONFIG' not in os.environ:
    os.environ['FLASK_CONFIG'] = '{{ appname }}.config.Development'

app.run(host='0.0.0.0', port=5000, debug=True)
