#
# course.py
#

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Course:
    id: int
    subject_code: str
    number: int
    suffix: str
    name: str
    description: str | None
    extra_information: str | None


@dataclass
class VCourseInfo:
    id: int
    subject_code: str
    subject_name: str
    number: int
    suffix: str
    credit: Decimal
    is_essay: bool
    category: str | None
    category_2: str | None
    name: str
    description: str | None
    extra_information: str | None


def get_v_course_info(db, subject_code: str, number: int) -> VCourseInfo | None:
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
