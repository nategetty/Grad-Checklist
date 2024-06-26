#
# test_course.py
#

from gradchecklist.course import *


def test_get_v_course(db):
    result = get_v_course(db, "COMPSCI", 1027)
    assert result is not None
    assert result.subject_code == "COMPSCI"
    assert result.number == 1027
    assert result.category == "C"


def test_get_v_course_no_records(db):
    assert get_v_course(db, "COMPSCI", 55555) is None


def test_get_v_course_by_name(db):
    result = get_v_course_by_name(db, "Computer Science", 1027)
    assert result is not None
    assert result.subject_code == "COMPSCI"
    assert result.number == 1027
    assert result.category == "C"


def test_insert_course(db):
    assert get_v_course(db, "COMPSCI", 9999) is None
    course = Course(subject_code="COMPSCI",
                    number=9999,
                    suffix="E",
                    name="NAME",
                    description="description",
                    extra_information="extra info")
    insert_course(db, course)
    assert get_v_course(db, "COMPSCI", 9999) is not None
