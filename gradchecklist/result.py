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
    status: Optional[int]
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

    def calc_min_grade(self):
        if not self.courses:
            return None

        grades = [course.grade for course in self.courses if isinstance(course.grade, (int, float))]
        return min(grades, default=None)


# Results modelled as a checklist.
@dataclass
class Result:
    # Summary
    modules: list[str] = field(default_factory=list)
    status: int = 0
    total_courses: ResultItem = field(default_factory=ResultItem)
    completed_courses: str = ""
    pending_courses: str = ""

    def add_module(self, module_name: str):
        self.modules.append(module_name)

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

    def calculate_min_grade(self):
        admission_min_grade_vals = [grade for grade in [req.calc_min_grade() for req in self.admission_requirements] if
                                    grade is not None]
        module_min_grade_vals = [grade for grade in [req.calc_min_grade() for req in self.module_requirements] if
                                 grade is not None]

        temp_admission_min = min(admission_min_grade_vals) if admission_min_grade_vals else None
        temp_module_min = min(module_min_grade_vals) if module_min_grade_vals else None

        self.principal_courses_lowest_grade.value = temp_admission_min
        self.module_lowest_grade.value = temp_module_min

        self.lowest_grade.value = min(temp_admission_min, temp_module_min)

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
        self.total_courses.value = len(combined_list)

    def setModuleStatus(self):
        if self.module_average.required_value is None or self.module_average.value is None:
            self.module_average.status = 0
        else:
            self.module_average.status = 1 if self.module_average.required_value <= self.module_average.value else 0

        if self.module_lowest_grade.required_value is None or self.module_lowest_grade.value is None:
            self.module_lowest_grade.status = 0
        else:
            self.module_lowest_grade.status = 1 if self.module_lowest_grade.required_value <= self.module_lowest_grade.value else 0

        if self.principal_courses_average.required_value is None or self.principal_courses_average.value is None:
            self.principal_courses_average.status = 0
        else:
            self.principal_courses_average.status = 1 if self.principal_courses_average.required_value <= self.principal_courses_average.value else 0

        if self.principal_courses_lowest_grade.required_value is None or self.principal_courses_lowest_grade.value is None:
            self.principal_courses_lowest_grade.status = 0
        else:
            self.principal_courses_lowest_grade.status = 1 if self.principal_courses_lowest_grade.required_value <= self.principal_courses_lowest_grade.value else 0

        if self.cumulative_average.required_value is None or self.cumulative_average.value is None:
            self.cumulative_average.status = 0
        else:
            self.cumulative_average.status = 1 if self.cumulative_average.required_value <= self.cumulative_average.value else 0

        if self.lowest_grade.required_value is None or self.lowest_grade.value is None:
            self.lowest_grade.status = 0
        else:
            self.lowest_grade.status = 1 if self.lowest_grade.required_value <= self.lowest_grade.value else 0

    def setFirstYearReqStatus(self):
        if (self.first_year_courses.value is None or self.first_year_courses.required_value is None or
                self.first_year_courses.value < self.first_year_courses.required_value):
            self.first_year_courses.status = 0
        else:
            self.first_year_courses.status = 1

        if (self.first_year_different_subjects.value is None or self.first_year_different_subjects.value <
                self.first_year_different_subjects.required_value):
            self.first_year_different_subjects.status = 0
        else:
            self.first_year_different_subjects.status = 1

        if (self.first_year_one_subject_limit.value is None or self.first_year_one_subject_limit.value >
                self.first_year_one_subject_limit.required_value):
            self.first_year_one_subject_limit.status = 0
        else:
            self.first_year_one_subject_limit.status = 1

    def setSeniorYearReqStatus(self):
        if (self.senior_courses.value is None or self.senior_courses.required_value is None or self.senior_courses.value
                < self.senior_courses.required_value):
            self.senior_courses.status = 0
        else:
            self.senior_courses.status = 1

    def setEssayReqStatus(self):
        if (self.senior_essay_courses.value is None or self.senior_essay_courses.required_value is None or
                self.senior_essay_courses.value < self.senior_essay_courses.required_value):
            self.senior_essay_courses.status = 0
        else:
            self.senior_essay_courses.status = 1
        if (self.total_essay_courses.value is None or self.total_essay_courses.required_value is None or
                self.total_essay_courses.value < self.total_essay_courses.required_value):
            self.total_essay_courses.status = 0
        else:
            self.total_essay_courses.status = 1

    def setBreadthReqStatus(self):
        if (self.category_a.value is None or self.category_a.required_value is None or
                self.category_a.value < self.category_a.required_value):
            self.category_a.status = 0
        else:
            self.category_a.status = 1

        if (self.category_b.value is None or self.category_b.required_value is None or
                self.category_b.value < self.category_b.required_value):
            self.category_b.status = 0
        else:
            self.category_b.status = 1

        if (self.category_c.value is None or self.category_c.required_value is None or
                self.category_c.value < self.category_c.required_value):
            self.category_c.status = 0
        else:
            self.category_c.status = 1