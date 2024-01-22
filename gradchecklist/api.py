#
# api.py
# API functions.
#

from flask import Blueprint, jsonify, request
from .db import get_db

bp = Blueprint("api", __name__)


@bp.post("/upload-transcript")
def upload_transcript():
    return "Hello world!"


@bp.route("/test")
def test():
    db = get_db()
    db.execute("SELECT * FROM Course;")
    return jsonify(db.fetchall())
