from .module import get_module
from .db import get_db
from .student import Student
from .result import *

def moduleRequirementsFromDB():
    db = get_db()
    name = 'HONOURS SPECIALIZATION IN COMPUTER SCIENCE'
    module = get_module(db, name)
    return module

def createResult():
    result = Result()
    return result

def courseComparison(students, module):
    result = createResult()

    if not module.requirements:
        return result

    for student in students:

        for requirement in module.requirements:

            completedCount = Decimal(0)
            pendingCount = Decimal(0)

            # Account for Non-Honours
            minimumGrade = requirement.minimum_grade if requirement.minimum_grade is not None else 60

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

            setResultsRequiredAVGandLowestGrade(module, result)

            if requirement.is_admission:            
                result.admission_requirements.append(resultRequirement)
            else:
                result.module_requirements.append(resultRequirement)

            for course in requirement.courses: 
                
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
                        if tempCourse[1].isdigit():
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
                            pendingCount += course.credit
                    elif tempCourse[1] in ['F', 'WDN', 'RNC']:
                        resultCourse.status = 0
                        resultRequirement.status = 0
                    elif tempCourse[1] == 'PAS' or int(tempCourse[1]) >= minimumGrade:
                        resultCourse.status = 1
                        completedCount += course.credit
                    else:
                        resultCourse.status = 0
                        resultRequirement.status = 0
                elif not resultRequirement.is_from:
                    resultCourse.status = 0
                    resultRequirement.status = 0         

        if completedCount >= requirement.total_credit:
            resultRequirement.status = 1
        elif completedCount + pendingCount >= requirement.total_credit:
            resultRequirement.status = 2
        else:
            resultRequirement.status = 0

    result.calculate_min_grade()
    admission_course_grades = result.calculate_requirement_avg(result.admission_requirements, result.principal_courses_average)
    module_course_grades = result.calculate_requirement_avg(result.module_requirements, result.module_average)
    result.calculate_overall_avg(admission_course_grades,module_course_grades)
    result.setModuleStatus()
        
    return result

def setResultsRequiredAVGandLowestGrade(module, result):
    is_honours = "HONOURS" in module.name

    if is_honours:
        result.principal_courses_lowest_grade.required_value = 60
        result.principal_courses_average.required_value = 70
        result.module_average.required_value = 70
        result.module_lowest_grade.required_value = 60
        result.cumulative_average.required_value = 70
        result.lowest_grade.required_value = 60
    else:
        result.principal_courses_lowest_grade.required_value = 60
        result.principal_courses_average.required_value = None
        result.module_average.required_value = None
        result.module_lowest_grade.required_value = 50
        result.cumulative_average.required_value = None
        result.lowest_grade.required_value = 50
