#
# views.py
# View functions.
#

from flask import Blueprint

bp = Blueprint("views", __name__)

@bp.post("/upload-transcript")
def upload_transcript():
    return "Hello world!"
