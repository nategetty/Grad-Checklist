#
# course.py
#

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from .prerequisite import Prerequisite


@dataclass
class Course:
    id: int = 0
    subject_code: str = ""
    number: int = 0
    suffix: str = ""
    name: str = ""
    description: Optional[str] = ""
    extra_information: Optional[str] = ""
    prerequisites: list[Prerequisite] = field(default_factory=list)
    antirequisites: list["Course"] = field(default_factory=list)


@dataclass
class VCourse:
    id: int
    subject_code: str
    subject_name: str
    number: int
    suffix: str
    credit: Decimal
    is_essay: bool
    category: Optional[str]
    category_2: Optional[str]
    name: str
    description: Optional[str]
    extra_information: Optional[str]


# Finds and returns the course with the given subject code and number. Returns None if no matching course is found.
def get_v_course(db, subject_code: str, number: int) -> Optional[VCourse]:
    with db.cursor() as c:
        c.execute("SELECT * FROM VCourse WHERE subject_code=%s AND number=%s",
                  (subject_code, number))
        course = c.fetchone()
    if course is None:
        return None
    else:
        return VCourse(*course)
    

# Finds and returns the course with the given subject name and number. Returns None if no matching course is found.
def get_v_course_by_name(db, subject_name: str, number: int) -> Optional[VCourse]:
    with db.cursor() as c:
        c.execute("SELECT * FROM VCourse WHERE subject_name=%s AND number=%s",
                  (subject_name, number))
        course = c.fetchone()
    if course is None:
        return None
    else:
        return VCourse(*course)


# Inserts course into the database.
# Raises errors if the insert query fails.
def insert_course(db, course: Course):
    try:
        with db.cursor() as c:
            c.execute("INSERT INTO Course VALUES (%s,%s,%s,%s,%s,%s,%s)",
                      list(vars(course).values()))
        db.commit()
    except:
        db.rollback()
        raise
