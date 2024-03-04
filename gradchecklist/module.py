#
# module.py
#

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from .course import VCourse


@dataclass
class ModuleRequirementSubject:
    subject_code: str = ""
    minimum_level: int = 0


# Set of courses required by a module.
# Example from academic calendar:
#   "0.5 course from: Computer Science 1027A/B or Computer Science 1037A/B (in either case with a mark of at least 65%)"
@dataclass
class ModuleRequirement:
    id: int = 0
    module_id: int = 0
    total_credit: Decimal = Decimal(0)
    minimum_grade: Optional[int] = None
    required_average: Optional[int] = None
    is_admission: bool = False
    courses: list[VCourse] = field(default_factory=list)
    subjects: list[ModuleRequirementSubject] = field(default_factory=list)


# Program/module. E.g. SPECIALIZATION IN COMPUTER SCIENCE
@dataclass
class Module:
    id: int = 0
    name: str = ""
    requirements: list[ModuleRequirement] = field(default_factory=list)


# Finds and returns the module with the given name. Returns None if no module was found.
def get_module(db, name: str) -> Optional[Module]:
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
            c.execute("SELECT VCourse.* FROM ModuleRequirementCourse JOIN VCourse ON id=course_id WHERE requirement_id=%s",
                  (req[0],))
            courses = [VCourse(*course) for course in c.fetchall()]
        with db.cursor() as c:
            c.execute("SELECT subject_code, minimum_level FROM ModuleRequirementSubject WHERE requirement_id=%s",
                      (req[0],))
            subjects = [ModuleRequirementSubject(*subject) for subject in c.fetchall()]
        module.requirements.append(ModuleRequirement(*req, courses, subjects))

    return module


# Inserts module into the database.
# Raises errors if the insert query fails.
def insert_module(db, module: Module):
    try:
        with db.cursor() as c:
            c.execute("INSERT INTO Module VALUES (%s,%s)",
                      (module.id, module.name))
            module_id = c.lastrowid
            for req in module.requirements:
                c.execute("INSERT INTO ModuleRequirement VALUES (%s,%s,%s,%s,%s,%s)",
                          (req.id, module_id, req.total_credit, req.minimum_grade, req.required_average, req.is_admission))
                req_id = c.lastrowid
                for course in req.courses:
                    c.execute("INSERT INTO ModuleRequirementCourse VALUES (%s,%s)",
                              (req_id, course.id))
                for subject in req.subjects:
                    c.execute("INSERT INTO ModuleRequirementSubject VALUES (%s,%s,%s,%s)",
                              (0, req_id, subject.subject_code, subject.minimum_level))
        db.commit()
    except:
        db.rollback()
        raise
