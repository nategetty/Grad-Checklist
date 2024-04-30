from collections import defaultdict
from .course import VCourse
from .module import Module
from .result import *
from .transcript_scrapper import Student


# Removes a course from the module requirements.
def remove_req_course(module: Module, subject_code: str, course_number: int):
    course_to_remove = None
    for req in module.requirements:
        for course in req.courses:
            if course.subject_code == subject_code and course.number == course_number:
                course_to_remove = course
                break
        
        if course_to_remove is not None:
            req.courses.remove(course_to_remove)
            if not req.courses:
                module.requirements.remove(req)
            break


# Finds the lowest grade in the top total_credit courses.
def find_lowest_grade(courses, total_credit: Decimal, result_item: ResultItem):
    if not courses:
        return
    
    courses.sort(key=lambda c: c[1], reverse=True)
    lowest_grade = None
    credits = Decimal(0)
    for course, grade in courses:
        grade = int(grade)
        if lowest_grade is None or grade < lowest_grade:
            lowest_grade = grade
        credits += course.credit
        if credits >= total_credit:
            break

    result_item.value = lowest_grade
    if lowest_grade is not None:
        if lowest_grade >= result_item.required_value:
            result_item.status = 1
        else:
            result_item.status = 0


# Computes the average of the top total_credit courses.
def compute_average(courses, total_credit: Decimal, result_item: ResultItem):
    if not courses or total_credit == 0:
        return
    
    courses.sort(key=lambda c: c[1], reverse=True)
    s = Decimal(0)
    n = 0
    credits = Decimal(0)
    for course, grade in courses:
        s += Decimal(grade)
        n += 1
        credits += course.credit
        if credits >= total_credit:
            break
    average = s / n

    result_item.value = f"{average:.2f}"
    if average >= Decimal(result_item.required_value):
        result_item.status = 1
    else:
        result_item.status = 0


# Checks module and admission requirements.
def courseComparison(result: Result, students: list[Student]):
    first_year_courses = Decimal(0)
    first_year_courses_subjects = defaultdict(Decimal)
    first_year_A, first_year_B, first_year_C = Decimal(0), Decimal(0), Decimal(0)
    total_year_A, total_year_B, total_year_C = Decimal(0), Decimal(0), Decimal(0)
    senior_courses = Decimal(0)
    senior_essay_courses = Decimal(0)
    essay_courses = Decimal(0)

    module = None
    for student in students:
        all_completed_courses = list(filter(lambda c: c[1] is not None and c[1].isnumeric(), student.courses))

        if not student.itr:
            continue

        module = student.itr[0]
        if module.name == "HONOURS SPECIALIZATION IN COMPUTER SCIENCE":
            if "MINOR IN SOFTWARE ENGINEERING" in (m.name for m in student.itr):
                remove_req_course(module, "COMPSCI", 4490)
            elif "MINOR IN GAME DEVELOPMENT" in (m.name for m in student.itr):
                remove_req_course(module, "COMPSCI", 4490)

        result.modules = [module.name.title().replace("In", "in") for module in student.itr]
        
        result.principal_courses.value = 0
        result.module_courses.value = 0

        admission_completed_courses = []
        module_completed_courses = []

        # Combine other module requirements with the main module.
        # TODO It's probably better to keep them separate. Needs UI work.
        for other_module in student.itr[1:]:
            module.requirements += other_module.requirements

        for requirement in module.requirements:
            req_completed_courses = []

            completedCount = Decimal(0)
            pendingCount = Decimal(0)

            courseSum = sum(course.credit for course in requirement.courses)

            resultRequirement = createResultRequirement(requirement, courseSum)
            honoursFlag = setResultsRequiredAVGandLowestGrade(module, result)
            minimumGrade = setRequirementMinGrade(requirement, honoursFlag)
            isAdmission = appendResultRequirementToResult(result, requirement, resultRequirement)

            for course in requirement.courses:
                resultCourse = createResultCourse(resultRequirement, course)

                tempCourse = None

                for studentCourse in student.courses:
                    if course == studentCourse[0]:
                        tempCourse = studentCourse
                        if tempCourse[1] is not None and tempCourse[1].isdigit():
                            resultCourse.grade = int(tempCourse[1])
                        else:
                            resultCourse.grade = tempCourse[1]
                        student.courses.remove(studentCourse)
                        break

                if tempCourse is not None:
                    if tempCourse[1] is None:
                        resultCourse.status = 2
                        if resultRequirement.status == 1:
                            resultRequirement.status = 2
                        if completedCount + pendingCount < requirement.total_credit:
                            incrementRequirementCount(result, isAdmission, tempCourse[0].credit)
                        pendingCount += course.credit

                    elif tempCourse[1] in ['F', 'WDN', 'RNC']:
                        resultCourse.status = 0
                    elif tempCourse[1] == 'PAS' or tempCourse[1] == 'CR' or int(tempCourse[1]) >= minimumGrade:
                        resultCourse.status = 1
                        if completedCount + pendingCount < requirement.total_credit:
                            incrementRequirementCount(result, isAdmission, tempCourse[0].credit)
                        completedCount += course.credit
                        if tempCourse[1].isnumeric():
                            req_completed_courses.append(tempCourse)
                            if requirement.is_admission:
                                admission_completed_courses.append(tempCourse)
                            else:
                                module_completed_courses.append(tempCourse)

                        if course.number >= 2000:
                            senior_courses += course.credit
                            if course.suffix in ['E', 'F', 'G', 'F/G']:
                                senior_essay_courses += course.credit
                                essay_courses += course.credit
                            # fix later, currently operate under single category assumption
                            if course.category == 'A':
                                total_year_A += course.credit
                            elif course.category == 'B':
                                total_year_B += course.credit
                            else:
                                total_year_C += course.credit
                        else:
                            first_year_courses += course.credit
                            first_year_courses_subjects[course.subject_code] += course.credit
                            if course.suffix in ['E', 'F', 'G', 'F/G']:
                                essay_courses += course.credit
                            # fix later, currently operate under single category assumption
                            # Ex: women's studies (A & B)
                            if course.category == 'A':
                                first_year_A += course.credit
                                total_year_A += course.credit
                            elif course.category == 'B':
                                first_year_B += course.credit
                                total_year_B += course.credit
                            else:
                                first_year_C += course.credit
                                total_year_C += course.credit
                    else:
                        resultCourse.status = 0
                        if tempCourse[1].isnumeric():
                            req_completed_courses.append(tempCourse)
                            if requirement.is_admission:
                                admission_completed_courses.append(tempCourse)
                            else:
                                module_completed_courses.append(tempCourse)
                elif not resultRequirement.is_from:
                    resultCourse.status = 0
                    resultRequirement.status = 0
                    result.status = 0

            for subject in requirement.subjects:
                result_subject = ResultSubject(subject_name=subject.subject_name, minimum_level=subject.minimum_level)
                resultRequirement.subjects.append(result_subject)
                for course, grade in student.courses:
                    if course.subject_code == subject.subject_code and course.number >= subject.minimum_level:
                        result_course = ResultCourse(
                            None,
                            int(grade) if grade is not None and grade.isnumeric() else grade,
                            course.subject_name,
                            course.number,
                            course.suffix
                        )
                        result_subject.courses.append(result_course)

                        if grade is None:
                            result_course.status = 2
                            if completedCount + pendingCount < requirement.total_credit:
                                incrementRequirementCount(result, isAdmission, course.credit)
                            pendingCount += course.credit
                        elif grade in ['F', 'WDN', 'RNC']:
                            result_course.status = 0
                        elif grade == 'PAS' or grade == 'CR' or int(grade) >= minimumGrade:
                            result_course.status = 1
                            if completedCount + pendingCount < requirement.total_credit:
                                incrementRequirementCount(result, isAdmission, course.credit)
                            completedCount += course.credit
                            if grade.isnumeric():
                                req_completed_courses.append((course, grade))
                            if requirement.is_admission:
                                admission_completed_courses.append((course, grade))
                            else:
                                module_completed_courses.append((course, grade))
                        else:
                            result_course.status = 0

            if completedCount >= requirement.total_credit:
                resultRequirement.status = 1
            elif completedCount + pendingCount >= requirement.total_credit:
                resultRequirement.status = 2
                if result.status == 1:
                    result.status = 2
            else:
                resultRequirement.status = 0
                result.status = 0

            if requirement.minimum_grade is not None:
                find_lowest_grade(req_completed_courses, requirement.total_credit, resultRequirement.minimum_grade)

    compute_average(all_completed_courses, Decimal(20.0), result.cumulative_average)
    find_lowest_grade(all_completed_courses, Decimal(20.0), result.lowest_grade)

    if module is not None:
        result.principal_courses.required_value = sum((req.total_credit for req in filter(lambda req: req.is_admission, module.requirements)))
        result.module_courses.required_value = sum((req.total_credit for req in filter(lambda req: not req.is_admission, module.requirements)))

        compute_average(admission_completed_courses, result.principal_courses.required_value, result.principal_courses_average)
        compute_average(module_completed_courses, result.module_courses.required_value, result.module_average)

        find_lowest_grade(admission_completed_courses, result.principal_courses.required_value, result.principal_courses_lowest_grade)
        find_lowest_grade(module_completed_courses, result.module_courses.required_value, result.module_lowest_grade)

    return result


def incrementRequirementCount(result, isAdmission, credit: Decimal):
    if isAdmission:
        result.principal_courses.value += credit
    else:
        result.module_courses.value += credit


def createResultCourse(resultRequirement, course):
    resultCourse = ResultCourse(
        None,
        None,
        course.subject_name,
        course.number,
        course.suffix
    )
    resultRequirement.courses.append(resultCourse)
    return resultCourse


def createResultRequirement(requirement, courseSum):
    isFrom = not requirement.total_credit == courseSum

    if requirement.minimum_grade is not None:
        resultItemMin = ResultItem(required_value=requirement.minimum_grade)
    else:
        resultItemMin = None
    if requirement.required_average is not None:
        resultItemAvg = ResultItem(required_value=requirement.required_average)
    else:
        resultItemAvg = None

    resultRequirement = ResultRequirement(
        1,
        requirement.total_credit,
        isFrom,
        resultItemMin,
        resultItemAvg
    )
    
    return resultRequirement


def appendResultRequirementToResult(result, requirement, resultRequirement):
    if requirement.is_admission:
        result.admission_requirements.append(resultRequirement)
        isAdmission = True
    else:
        result.module_requirements.append(resultRequirement)
        isAdmission = False
    return isAdmission


def setRequirementMinGrade(requirement, honoursFlag):
    if honoursFlag: 
        minimumGrade = requirement.minimum_grade if requirement.minimum_grade is not None else 60
    else:
        minimumGrade = requirement.minimum_grade if requirement.minimum_grade is not None else 50
    return minimumGrade


def setResultsRequiredAVGandLowestGrade(module, result):
    is_honours = "HONOURS" in module.name

    if is_honours:
        result.principal_courses_lowest_grade.required_value = 60
        result.principal_courses_average.required_value = 70
        result.module_average.required_value = 70
        result.module_lowest_grade.required_value = 60
        result.cumulative_average.required_value = 65
        result.lowest_grade.required_value = 50
        return True
    else:
        result.principal_courses_lowest_grade.required_value = 60
        result.principal_courses_average.required_value = 50
        result.module_average.required_value = 50
        result.module_lowest_grade.required_value = 50
        result.cumulative_average.required_value = 60
        result.lowest_grade.required_value = 50
        return False
