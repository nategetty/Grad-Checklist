#
# api.py
# API functions.
#

from flask import Blueprint, jsonify, request
from .db import get_db
from .course import Course, get_v_course_info, insert_course
from .module import get_module

bp = Blueprint("api", __name__)


@bp.post("/upload-transcript")
def upload_transcript():
    return "Hello world!"

@bp.route("/test-reqs")
def reqs():
    module = get_module(get_db(), "MAJOR IN COMPUTER SCIENCE")
    return jsonify(module.requirements)

@bp.route("/module")
def module():
    return jsonify(get_module(get_db(), "MAJOR IN COMPUTER SCIENCE"))
