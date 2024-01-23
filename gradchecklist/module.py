#
# module.py
#

from dataclasses import dataclass, field
from decimal import Decimal
from .course import VCourseInfo


@dataclass
class ModuleRequirement:
    id: int
    module_id: int
    total_credit: Decimal
    minimum_grade: int
    required_average: int
    is_admission: bool
    courses: list[VCourseInfo] = field(default_factory=list)


@dataclass
class Module:
    id: int
    name: str
    requirements: list[ModuleRequirement] = field(default_factory=list)


def get_module(db, name: str):
    with db.cursor() as c:
        c.execute("SELECT * FROM Module WHERE name=%s", (name,))
        module = c.fetchone()
    if module is None:
        return None
    module = Module(*module)

    with db.cursor() as c:
        c.execute("SELECT * FROM ModuleRequirement WHERE module_id=%s", (module.id,))
        reqs = c.fetchall()
    for req in reqs:
        with db.cursor() as c:
            c.execute("SELECT VCourseInfo.* FROM ModuleRequirementCourse JOIN VCourseInfo ON id=course_id WHERE requirement_id=%s",
                  (req[0],))
            courses = [VCourseInfo(*course) for course in c.fetchall()]
        module.requirements.append(ModuleRequirement(*req, courses))

    return module


def insert_module(db, module: Module):
    try:
        with db.cursor() as c:
            c.execute("INSERT INTO Module VALUES (%s,%s)",
                      vars(module))
            for req in module.requirements:
                c.execute("INSERT INTO ModuleRequirement VALUES (%s,%s,%s,%s,%s,%s)",
                          vars(req))
                for course in req.courses:
                    c.execute("INSERT INTO ModuleRequirementCourse VALUES (%s,%s)",
                              (req.id, course.id))
        db.commit()
    except:
        db.rollback()
