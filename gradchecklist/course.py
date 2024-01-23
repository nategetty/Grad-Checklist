#
# course.py
#

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Course:
    id: int
    subject_code: str
    number: int
    suffix: str
    name: str
    description: str
    extra_information: str


@dataclass
class VCourseInfo:
    id: int
    subject_code: str
    subject_name: str
    number: int
    suffix: str
    credit: Decimal
    is_essay: bool
    category: str
    category_2: str
    name: str
    description: str
    extra_information: str


def get_v_course_info(db, subject_code: str, number: int) -> Optional[VCourseInfo]:
    c = db.cursor()
    c.execute("SELECT * FROM VCourseInfo WHERE subject_code=%s AND number=%s",
              (subject_code, number))
    course = c.fetchone()
    if course is None:
        return None
    else:
        return VCourseInfo(*course)


def insert_course(db, course: Course):
    try:
        with db.cursor() as c:
            c.execute("INSERT INTO Course VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    vars(course).values())
        db.commit()
    except:
        db.rollback()
