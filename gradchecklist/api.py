#
# api.py
# API functions.
#

from flask import Blueprint
from flask import request

bp = Blueprint("api", __name__)

@bp.post("/upload-transcript")
def upload_transcript():
    return "Hello world!"
