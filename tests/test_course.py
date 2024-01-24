#
# test_course.py
#

from gradchecklist.course import *


def test_get_course(db):
    result = get_v_course_info(db, "COMPSCI", 1027)
    assert result is not None
    assert result.subject_code == "COMPSCI"
    assert result.number == 1027
    assert result.category == "C"


def test_get_course_no_records(db):
    assert get_v_course_info(db, "COMPSCI", 19999) is None


def test_insert_course(db):
    assert get_v_course_info(db, "COMPSCI", 19999) is None
    course = Course(0, "COMPSCI", 19999, "E", "NAME", "description", "extra info")
    insert_course(db, course)
    assert get_v_course_info(db, "COMPSCI", 19999) is not None
