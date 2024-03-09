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
    COMPLETE = 1    # Complete, all grades received.
    PENDING = 2     # Complete, grades not received yet.


# Generic checklist item.
@dataclass
class ResultItem:
    status: Optional[int] = None
    value: Optional[str] = None           # (If applicable) courses completed OR average acheived
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
    status: int = 0
    total_courses: ResultItem = ResultItem()
    completed_courses: str = ""
    pending_courses: str = ""

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
    
    def calculate_min_grade(self):
        admission_min_grade_vals = [grade for grade in [req.calc_min_grade() for req in self.admission_requirements] if grade is not None]
        module_min_grade_vals = [grade for grade in [req.calc_min_grade() for req in self.module_requirements] if grade is not None]

        temp_admission_min = min(admission_min_grade_vals) if admission_min_grade_vals else None
        temp_module_min = min(module_min_grade_vals) if module_min_grade_vals else None

        self.principal_courses_lowest_grade.value = temp_admission_min
        self.module_lowest_grade.value = temp_module_min

        self.lowest_grade.value = min(temp_admission_min, temp_module_min)


    def calculate_requirement_avg(self, req_list, result_item_average):
        all_course_grades = []

        for req in req_list:
            if req.courses:
                course_avg_vals = [float(course.grade) if isinstance(course.grade, (int, float)) else float(course.grade[:-1]) if course.grade is not None and course.grade[:-1].isdigit() else None for course in req.courses]
                valid_course_grades = [grade for grade in course_avg_vals if grade is not None]
                all_course_grades.extend(valid_course_grades)

        result_item_average.value = round(mean(all_course_grades) if all_course_grades else 0)
        return all_course_grades
    
    def calculate_overall_avg(self, admission_grade_list, module_grade_list):
        combined_list = admission_grade_list + module_grade_list

        total_average = sum(combined_list) / len(combined_list)
        self.cumulative_average.value = round(total_average)

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