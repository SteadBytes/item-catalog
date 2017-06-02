from app import app
from werkzeug.serving import make_ssl_devcert
make_ssl_devcert('./ssl', host='localhost')
app.debug = True
app.run(host='0.0.0.0', port=5000, ssl_context=('./ssl.crt', './ssl.key'))
