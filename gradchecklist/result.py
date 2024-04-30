#
# result.py
#

from enum import Enum
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


# Requirement status.
# This enum is unused because the JSON serializer cannot handle enums. Instead int is used for status codes.
class Status(Enum):
    INCOMPLETE = 0  # Not complete / not on transcript.
    COMPLETE = 1    # Complete, all grades received.
    PENDING = 2     # Complete, grades not received yet.


# Generic checklist item.
@dataclass
class ResultItem:
    status: Optional[int] = None
    value: Optional[str] = None  # (If applicable) courses completed OR average acheived
    required_value: Optional[str] = None  # (If applicable) courses required OR minimum average required


# Checklist course.
@dataclass
class ResultCourse():
    status: Optional[int]
    grade: Optional[str]
    subject_name: str
    number: int
    suffix: str


# Checklist subject (i.e. courses at the XXXX level or above)
@dataclass
class ResultSubject():
    subject_name: str
    minimum_level: int
    courses: list[ResultCourse] = field(default_factory=list)


# Checklist (module/admission) requirement.
@dataclass
class ResultRequirement():
    status: Optional[int]
    total_credit: Decimal
    is_from: bool
    minimum_grade: Optional[ResultItem] = None
    required_average: Optional[ResultItem] = None
    courses: list[ResultCourse] = field(default_factory=list)
    subjects: list[ResultSubject] = field(default_factory=list)


# Results modelled as a checklist.
@dataclass
class Result:
    # Summary
    modules: list[str] = field(default_factory=list)
    status: int = 1
    total_courses: ResultItem = field(default_factory=ResultItem)
    completed_courses: str = ""
    pending_courses: str = ""

    # First year requirements
    first_year_courses: ResultItem = field(default_factory=ResultItem)
    first_year_different_subjects: ResultItem = field(default_factory=ResultItem)
    first_year_one_subject_limit: ResultItem = field(default_factory=ResultItem)

    # Senior course requirements
    senior_courses: ResultItem = field(default_factory=ResultItem)

    # Average requirements
    cumulative_average: ResultItem = field(default_factory=ResultItem)
    lowest_grade: ResultItem = field(default_factory=ResultItem)

    # Breadth requirements
    category_a: ResultItem = field(default_factory=ResultItem)
    category_b: ResultItem = field(default_factory=ResultItem)
    category_c: ResultItem = field(default_factory=ResultItem)

    # Essay requirements 
    total_essay_courses: ResultItem = field(default_factory=ResultItem)
    senior_essay_courses: ResultItem = field(default_factory=ResultItem)

    # Admission requirements
    principal_courses: ResultItem = field(default_factory=ResultItem)
    principal_courses_average: ResultItem = field(default_factory=ResultItem)
    principal_courses_lowest_grade: ResultItem = field(default_factory=ResultItem)
    admission_requirements: list[ResultRequirement] = field(default_factory=list)

    # Module requirements
    module_courses: ResultItem = field(default_factory=ResultItem)
    module_average: ResultItem = field(default_factory=ResultItem)
    module_lowest_grade: ResultItem = field(default_factory=ResultItem)
    module_requirements: list[ResultRequirement] = field(default_factory=list)
