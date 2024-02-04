#
# api.py
# API functions.
#

from flask import Blueprint, jsonify, request
from .db import get_db
from .course import Course, get_v_course, insert_course
from .module import get_module
from . import transcript_scrapper
from .module_logic import *

bp = Blueprint("api", __name__)

@bp.post("/upload-transcript")
def upload_transcript():
    file_obj = request.files["file"]
    student = transcript_scrapper.main(file_obj)
    module = moduleRequirementsFromDB()
    result = courseComparison(student, module)
    return jsonify(result)

@bp.route("/module")
def module():
    return jsonify(get_module(get_db(), "HONOURS SPECIALIZATION IN COMPUTER SCIENCE"))
