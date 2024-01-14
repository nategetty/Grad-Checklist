#
# __init__.py
# Package initializer for the production server.
# Don't use this for development!
#

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

__version__ = "0.1"

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

from . import api
app.register_blueprint(api.bp)
