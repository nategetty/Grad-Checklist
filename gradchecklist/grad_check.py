#
# grad_check.py
# Graduation requirements checking.
#

from decimal import Decimal
from .course import VCourse
from .result import *
from .transcript_scrapper import Student

TOTAL_COURSES_REQUIRED = Decimal(20.0)
FIRST_YEAR_COURSES_REQUIRED = Decimal(5.0)
FIRST_YEAR_DIFFERENT_SUBJECTS_REQUIRED = 4
FIRST_YEAR_ONE_SUBJECT_LIMIT = Decimal(2.0)
SENIOR_COURSES_REQUIRED = Decimal(13.0)
CATEGORY_A_REQUIRED = Decimal(1.0)
CATEGORY_B_REQUIRED = Decimal(1.0)
CATEGORY_C_REQUIRED = Decimal(1.0)
TOTAL_ESSAY_COURSES_REQUIRED = Decimal(2.0)
SENIOR_ESSAY_COURSES_REQUIRED = Decimal(1.0)

MINIMUM_GRADE = 50
REQUIRED_AVERAGE = 60
MODULE_MINIMUM_GRADE = 50
MODULE_REQUIRED_AVERAGE = 60

HONOURS_MINIMUM_GRADE = 50
HONOURS_REQUIRED_AVERAGE = 65
HONOURS_MODULE_MINIMUM_GRADE = 60
HONOURS_MODULE_REQUIRED_AVERAGE = 70

def is_credited(grade: str) -> bool:
    return grade not in ["F", "FAI", "WDN", "SPC"]


def is_first_year(course: VCourse) -> bool:
    return 1000 <= course.number <= 1999


def is_senior(course: VCourse) -> bool:
    return 2000 <= course.number <= 4999


class CreditCount:
    def __init__(self):
        self.total = Decimal(0)
        self.pending = Decimal(0)

    def add(self, course, grade):
        self.total += course.credit
        if grade is None:
            self.pending += course.credit

    def create_item(self, required_courses: Decimal, result: Result) -> ResultItem:
        item = ResultItem(value=f"{self.total:.1f}", required_value=f"{required_courses:.1f}")
        if self.total - self.pending >= required_courses:
            item.status = 1
        elif self.total >= required_courses:
            item.status = 2
            if result.status == 1:
                result.status = 2
        else:
            item.status = 0
            result.status = 0
        return item
    

def credit_count(result: Result, student: Student):
    all_courses = CreditCount()

    first_year_courses = CreditCount()
    first_year_subjects = {}

    senior_courses = CreditCount()

    category_a = CreditCount()
    category_b = CreditCount()
    category_c = CreditCount()

    total_essay_courses = CreditCount()
    senior_essay_courses = CreditCount()

    for course, grade in student.courses:
        if course is None:
            continue
        if not is_credited(grade):
            continue

        # Summary
        all_courses.add(course, grade)

        # First year requirements, senior course requirements
        if is_first_year(course):
            first_year_courses.add(course, grade)
            if course.subject_code not in first_year_subjects:
                first_year_subjects[course.subject_code] = course.credit
            else:
                first_year_subjects[course.subject_code] += course.credit
        elif is_senior(course):
            senior_courses.add(course, grade)

        # Breadth requirements
        if course.category == "A":
            category_a.add(course, grade)
        elif course.category == "B":
            category_b.add(course, grade)
        elif course.category == "C":
            category_c.add(course, grade)

        # Essay requirements
        if course.is_essay:
            total_essay_courses.add(course, grade)
            if is_senior(course):
                senior_essay_courses.add(course, grade)

    # Summary
    result.total_courses = all_courses.create_item(TOTAL_COURSES_REQUIRED, result)
    result.completed_courses = f"{all_courses.total - all_courses.pending:.1f}"
    result.pending_courses = f"{all_courses.pending:.1f}"

    # First year requirements
    result.first_year_courses = first_year_courses.create_item(FIRST_YEAR_COURSES_REQUIRED, result)
    if len(first_year_subjects) >= FIRST_YEAR_DIFFERENT_SUBJECTS_REQUIRED:
        result.first_year_different_subjects.status = 1
    else:
        result.first_year_different_subjects.status = 0
    if max(first_year_subjects.values()) <= FIRST_YEAR_ONE_SUBJECT_LIMIT:
        result.first_year_one_subject_limit.status = 1
    else:
        result.first_year_one_subject_limit.status = 0

    # Senior course requirements
    result.senior_courses = senior_courses.create_item(SENIOR_COURSES_REQUIRED, result)

    # Breadth requirements
    result.category_a = category_a.create_item(CATEGORY_A_REQUIRED, result)
    result.category_b = category_b.create_item(CATEGORY_B_REQUIRED, result)
    result.category_c = category_c.create_item(CATEGORY_C_REQUIRED, result)

    # Essay requirements
    result.total_essay_courses = total_essay_courses.create_item(TOTAL_ESSAY_COURSES_REQUIRED, result)
    result.senior_essay_courses = senior_essay_courses.create_item(SENIOR_ESSAY_COURSES_REQUIRED, result)
