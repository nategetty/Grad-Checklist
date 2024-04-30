#
# api.py
# API functions.
#

from flask import Blueprint, jsonify, request
from .db import get_db
from .course import Course
from .module import get_module
from .transcript_scrapper import processTranscript
from .grad_check import grad_check

bp = Blueprint("api", __name__)


@bp.post("/upload-transcript")
def upload_transcript():
    file_obj = request.files["file"]
    students = processTranscript(file_obj)
    result = grad_check(students)
    return jsonify(result)


@bp.route("/module")
def module():
    return jsonify(get_module(get_db(), "HONOURS SPECIALIZATION IN COMPUTER SCIENCE"))
