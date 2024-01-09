#
# __init__.py
# Packet initializer for the production server.
# Don't use this for development!
#

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import views

__version__ = "0.1"

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
app.register_blueprint(views.bp)
