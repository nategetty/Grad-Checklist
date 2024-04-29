from collections import defaultdict
from .course import get_v_course
from .db import get_db
from .result import *

def createResult():
    result = Result()
    return result

def courseComparison(students):
    result = createResult()

    first_year_courses = Decimal(0)
    first_year_courses_subjects = defaultdict(Decimal)
    first_year_A, first_year_B, first_year_C = Decimal(0), Decimal(0), Decimal(0)
    total_year_A, total_year_B, total_year_C = Decimal(0), Decimal(0), Decimal(0)
    senior_courses = Decimal(0)
    senior_essay_courses = Decimal(0)
    essay_courses = Decimal(0)

    for student in students:

        module = student.itr[0]
        
        if not module.requirements:
            return result
        
        result.add_module(module.name)
        result.principal_courses.value = 0
        result.module_courses.value = 0

        for requirement in module.requirements:

            completedCount = Decimal(0)
            pendingCount = Decimal(0)

            courseSum = sum(course.credit for course in requirement.courses)

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
            
            honoursFlag = setResultsRequiredAVGandLowestGrade(module, result)

            if honoursFlag: 
                minimumGrade = requirement.minimum_grade if requirement.minimum_grade is not None else 60
            else:
                minimumGrade = requirement.minimum_grade if requirement.minimum_grade is not None else 50

            if requirement.is_admission:
                result.admission_requirements.append(resultRequirement)
                isAdmission = True
            else:
                result.module_requirements.append(resultRequirement)
                isAdmission = False

            courseCount = 0

            for course in requirement.courses:
                
                courseCount += 1
                vcourse = get_v_course(get_db(), course.subject_code, course.number)

                resultCourse = ResultCourse(
                    None,
                    None,
                    course.subject_name,
                    course.number,
                    course.suffix
                )

                resultRequirement.courses.append(resultCourse)

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
                        if resultRequirement.status != 0:
                            resultRequirement.status = 2
                            result.status = 2
                            pendingCount += course.credit
                            
                        if isAdmission:
                                result.principal_courses.value += 1
                        else:
                            result.module_courses.value += 1

                    elif tempCourse[1] in ['F', 'WDN', 'RNC']:
                        resultCourse.status = 0
                        result.status = 0
                    elif tempCourse[1] == 'PAS' or tempCourse[1] == 'CR' or int(tempCourse[1]) >= minimumGrade:
                        resultCourse.status = 1
                        completedCount += course.credit

                        if isAdmission:
                            result.principal_courses.value += 1
                        else:
                            result.module_courses.value += 1

                        if course.number >= 2000:
                            senior_courses += course.credit
                            if course.suffix in ['E', 'F', 'G', 'F/G']:
                                senior_essay_courses += course.credit
                                essay_courses += course.credit
                            # fix later, currently operate under single category assumption
                            if vcourse.category == 'A':
                                total_year_A += course.credit
                            elif vcourse.category == 'B':
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
                            if vcourse.category == 'A':
                                first_year_A += course.credit
                                total_year_A += course.credit
                            elif vcourse.category == 'B':
                                first_year_B += course.credit
                                total_year_B += course.credit
                            else:
                                first_year_C += course.credit
                                total_year_C += course.credit
                    else:
                        resultCourse.status = 0
                elif not resultRequirement.is_from:
                    resultCourse.status = 0
                    resultRequirement.status = 0

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
                            pendingCount += course.credit
                        elif grade in ['F', 'WDN', 'RNC']:
                            result_course.status = 0
                        elif grade == 'PAS' or grade == 'CR' or int(grade) >= minimumGrade:
                            result_course.status = 1
                            completedCount += course.credit
                        else:
                            result_course.status = 0

            if completedCount >= requirement.total_credit:
                resultRequirement.status = 1
            elif completedCount + pendingCount >= requirement.total_credit:
                resultRequirement.status = 2
            else:
                resultRequirement.status = 0

    # Bad results for course count and subject count due to lacking course data, set to string and normalize
    result.first_year_courses.value = first_year_courses
    result.first_year_courses.required_value = Decimal(5.0)
    result.first_year_different_subjects.value = len(first_year_courses_subjects)
    result.first_year_different_subjects.required_value = 4
    result.first_year_one_subject_limit.value = max(first_year_courses_subjects.values())
    result.first_year_one_subject_limit.required_value = Decimal(2.0)
    result.setFirstYearReqStatus()

    result.senior_courses.value = senior_courses
    result.senior_courses.required_value = Decimal(13.0)
    result.setSeniorYearReqStatus()

    result.senior_essay_courses.value = senior_essay_courses
    result.senior_essay_courses.required_value = Decimal(1.0)
    result.total_essay_courses.value = essay_courses
    result.total_essay_courses.required_value = Decimal(2.0)
    result.setEssayReqStatus()

    result.category_a.value = total_year_A
    result.category_a.required_value = Decimal(1.0)
    result.category_b.value = total_year_B
    result.category_b.required_value = Decimal(1.0)
    result.category_c.value = total_year_C
    result.category_c.required_value = Decimal(1.0)
    result.setBreadthReqStatus()

    result.calculate_min_grade()
    admission_course_grades = result.calculate_requirement_avg(result.admission_requirements, result.principal_courses_average)
    module_course_grades = result.calculate_requirement_avg(result.module_requirements, result.module_average)
    result.principal_courses.required_value = len(admission_course_grades)
    result.module_courses.required_value = len(module_course_grades)
    result.calculate_overall_avg(admission_course_grades, module_course_grades)
    result.total_courses.value = result.principal_courses.value + result.module_courses.value
    result.setAvgRequirementsStatus()

    return result

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
