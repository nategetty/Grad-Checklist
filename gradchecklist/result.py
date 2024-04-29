#
# result.py
#

from enum import Enum
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from statistics import mean
from .module import ModuleRequirement


# Requirement status.
class Status(Enum):
    INCOMPLETE = 0  # Not complete / not on transcript.
    COMPLETE = 1  # Complete, all grades received.
    PENDING = 2  # Complete, grades not received yet.


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

    def calculate_requirement_avg(self, req_list, result_item_average):
        all_course_grades = []

        for req in req_list:
            if req.courses:
                course_avg_vals = [float(course.grade) if isinstance(course.grade, (int, float)) else float(
                    course.grade[:-1]) if course.grade is not None and course.grade[:-1].isdigit() else None for course
                                   in req.courses]
                valid_course_grades = [grade for grade in course_avg_vals if grade is not None]
                all_course_grades.extend(valid_course_grades)

        result_item_average.value = round(mean(all_course_grades) if all_course_grades else 0)
        return all_course_grades

    def calculate_overall_avg(self, admission_grade_list, module_grade_list):
        combined_list = admission_grade_list + module_grade_list

        total_average = sum(combined_list) / len(combined_list)
        self.cumulative_average.value = round(total_average)
        self.total_courses.required_value = len(combined_list)  

    def setAdmissionRequirementStatus(self):
        if self.principal_courses.value < self.principal_courses.required_value:
            self.principal_courses.status = 0
            self.status = 0
        else:
            self.principal_courses.status = 1

        if self.principal_courses_average.value < self.principal_courses_average.required_value:
            self.principal_courses_average.status = 0
            self.status = 0
        else:
            self.principal_courses_average.status = 1

        if self.principal_courses_lowest_grade.value is not None:
            if self.principal_courses_lowest_grade.value < self.principal_courses_lowest_grade.required_value:
                self.principal_courses_lowest_grade.status = 0
            else:
                self.principal_courses_lowest_grade.status = 1

    def setModuleRequirementStatus(self):
        if self.module_courses.value < self.module_courses.required_value:
            self.module_courses.status = 0
            self.status = 0
        else:
            self.module_courses.status = 1

        if self.module_average.value < self.module_average.required_value:
            self.module_average.status = 0
            self.status = 0
        else:
            self.module_average.status = 1

        if self.module_lowest_grade.value is not None:
            if self.module_lowest_grade.value < self.module_lowest_grade.required_value:
                self.module_lowest_grade.status = 0
            else:
                self.module_lowest_grade.status = 1

    def setAvgRequirementsStatus(self):
        if self.cumulative_average.value < self.cumulative_average.required_value:
            self.cumulative_average.status = 0
            self.status = 0
        else:
            self.cumulative_average.status = 1

        if self.lowest_grade.value is not None:
            if self.lowest_grade.value < self.lowest_grade.required_value:
                self.lowest_grade.status = 0
                self.status = 0
            else:
                self.lowest_grade.status = 1
        if self.lowest_grade.value is not None:
            if self.lowest_grade.value < self.lowest_grade.required_value:
                self.lowest_grade.status = 0
                self.status = 0
            else:
                self.lowest_grade.status = 1
