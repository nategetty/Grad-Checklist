#
# test_subject.py
#

from gradchecklist.subject import *


def test_get_subject(db):
    result = get_subject(db, "COMPSCI")
    assert result is not None
    assert result.code == "COMPSCI"
    assert result.name == "Computer Science"
    assert result.category == "C"
    assert result.category_2 is None


def test_get_course_no_records(db):
    assert get_subject(db, "NOTACOURSE") is None


def test_get_all_subject_codes(db):
    subject_codes = get_all_subject_codes(db)
    assert "COMPSCI" in subject_codes


def test_insert_course(db):
    assert get_subject(db, "NEWSUBJ") is None
    subject = Subject(code="NEWSUBJ",
                      name="New Subject",
                      category="A")
    insert_subject(db, subject)
    assert get_subject(db, "NEWSUBJ") is not None
