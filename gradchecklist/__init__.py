#
# __init__.py
#

import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from . import api, db

__version__ = "0.2"


# Creates the Flask application for production.
def create_production_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    app.register_blueprint(api.bp)

    return app


# Creates the Flask application for development.
def create_dev_app():
    app = Flask(__name__,
                static_url_path="",
                static_folder="../www")
    app.register_blueprint(api.bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return app.send_static_file("html/pages/upload.html")
    
    @app.route("/<path>")
    def html_page(path):
        return app.send_static_file(f"html/pages/{path}.html")
    
    @app.route("/include/<path>")
    def html_include(path):
        return app.send_static_file(f"html/include/{path}.html")
    
    return app


# Application factory.
def create_app():
    if os.environ.get("ENV") == "production":
        app = create_production_app()
    else:
        app = create_dev_app()

    app.config.from_object("gradchecklist.config.DefaultConfig")
    app.config.from_envvar("PRODUCTION_CONFIG", silent=True)
    db.init_app(app)

    return app
