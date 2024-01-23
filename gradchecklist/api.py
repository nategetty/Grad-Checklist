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

@bp.route("/course")
def course():
    db = get_db()
    insert_course(db, Course(0, "COMPSCI", 6969, "E", "COURSE NAME", "description", "extra info"))
    return jsonify(get_v_course_info(db, "COMPSCI", 6969))

@bp.route("/module")
def module():
    return jsonify(get_module(get_db(), "MAJOR IN COMPUTER SCIENCE"))
