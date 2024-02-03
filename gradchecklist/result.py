#
# result.py
#

from enum import Enum
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from .module import ModuleRequirement


# Requirement status.
class Status(Enum):
    INCOMPLETE = 0  # Not complete / not on transcript.
    COMPLETE = 1    # Complete, all grades received.
    PENDING = 2     # Complete, grades not received yet.


# Generic checklist item.
@dataclass
class ResultItem:
    status: Optional[Status] = None
    value: Optional[str] = None           # (If applicable) courses completed OR average acheived
    required_value: Optional[str] = None  # (If applicable) courses required OR minimum average required


# Checklist course.
@dataclass
class ResultCourse(ResultItem):
    subject_name: str
    number: int
    suffix: str


# Checklist (module/admission) requirement.
@dataclass
class ResultRequirement(ResultItem):
    total_credit: Decimal
    is_from: bool
    courses: list[ResultCourse] = field(default_factory=list)


# Results modelled as a checklist.
@dataclass
class Result:
    # Summary
    status: Status = Status.INCOMPLETE
    total_courses: ResultItem = ResultItem()
    completed_courses: ResultItem = ResultItem()
    pending_courses: ResultItem = ResultItem()

    # First year requirements
    first_year_courses: ResultItem = ResultItem()
    first_year_different_subjects: ResultItem = ResultItem()
    first_year_one_subject_limit: ResultItem = ResultItem()

    # Senior course requirements
    senior_courses: ResultItem = ResultItem()

    # Average requirements
    cumulative_average: ResultItem = ResultItem()
    lowest_grade: ResultItem = ResultItem()

    # Breadth requirements
    category_a: ResultItem = ResultItem()
    category_b: ResultItem = ResultItem()
    category_c: ResultItem = ResultItem()

    # Essay requirements
    total_essay_courses: ResultItem = ResultItem()
    senior_essay_courses: ResultItem = ResultItem()

    # Admission requirements
    principal_courses: ResultItem = ResultItem()
    principal_courses_average: ResultItem = ResultItem()
    principal_courses_lowest_grade: ResultItem = ResultItem()
    admission_requirements: list[ResultRequirement] = field(default_factory=list)

    # Module requirements
    module_courses: ResultItem = ResultItem()
    module_average: ResultItem = ResultItem()
    module_lowest_grade: ResultItem = ResultItem()
    module_requirements: list[ResultRequirement] = field(default_factory=list)
