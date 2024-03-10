#
# prerequisite.py
#

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from .course import VCourse

@dataclass
class Prerequisite:
    id: int = 0
    course_id: int = 0
    total_credit: Decimal = Decimal(0)
    minimum_grade: Optional[int] = None
    alternative_to: Optional["Prerequisite"] = None
    courses: list[VCourse] = field(default_factory=list)
