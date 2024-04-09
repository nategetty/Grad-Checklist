#
# api.py
# API functions.
#

from flask import Blueprint, jsonify, request
from .db import get_db
from .course import Course
from .module import get_module
from . import transcript_scrapper
from .module_logic import *
from .grad_check import credit_count
from copy import deepcopy

bp = Blueprint("api", __name__)

@bp.post("/upload-transcript")
def upload_transcript():
    file_obj = request.files["file"]
    students = transcript_scrapper.processTranscript(file_obj)
    student_copy = deepcopy(students[0])
    result = courseComparison(students)
    credit_count(result, student_copy)
    return jsonify(result)

@bp.route("/module")
def module():
    return jsonify(get_module(get_db(), "HONOURS SPECIALIZATION IN COMPUTER SCIENCE"))
