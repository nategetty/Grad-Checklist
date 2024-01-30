#
# result.py
#

from dataclasses import dataclass
from decimal import Decimal
from .module import Module


@dataclass
class RequirementResult:
    status: str
    lowest_grade: int | None
    average: int | None


@dataclass
class Result:
    module: Module
    status: str
    category_a: Decimal = Decimal(0)
    category_b: Decimal = Decimal(0)
    category_c: Decimal = Decimal(0)
    total_essay: Decimal = Decimal(0)
    upper_year_essay: Decimal = Decimal(0)

