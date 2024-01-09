#
# views.py
# View functions.
#

from flask import Blueprint

bp = Blueprint("views", __name__)

@bp.route("/foo")
def foo():
    return "Hello world!"
