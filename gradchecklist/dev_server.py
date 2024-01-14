#
# dev_server.py
# Entry point for starting the development server.
#

from flask import Flask, current_app
import api


# Creates the development server application.
def create_app():
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


# Starts the development server.
def run():
    app = create_app()
    app.run(port=8080, debug=True)


if __name__ == "__main__":
    run()
