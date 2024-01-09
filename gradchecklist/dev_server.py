#
# dev_server.py
# Entry point for starting the development server.
#

from flask import Flask, current_app
import views


# Creates the development server application.
def create_app():
    app = Flask(__name__,
                static_url_path="",
                static_folder="../www")
    app.register_blueprint(views.bp)
    
    @app.route("/")
    def upload():
        return current_app.send_static_file("html/upload.html")
    
    return app


# Starts the development server.
def run():
    app = create_app()
    app.run(port=8080, debug=True)


if __name__ == "__main__":
    run()
