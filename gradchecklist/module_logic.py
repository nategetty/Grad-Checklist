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

def courseComparison(student, module):
    
    result = createResult()

    #(breadth requirements check before removing courses from list)

    for requirement in module.requirements:

        minimumGrade = 60
        completedCount = Decimal(0)
        pendingCount = Decimal(0)

        if requirement.minimum_grade is not None:
            minimumGrade = requirement.minimum_grade

        courseSum = 0
        for course in requirement.courses:
                courseSum += course.credit

        if requirement.total_credit == courseSum:
            isFrom = False
        else:
            isFrom = True

        resultRequirement = ResultRequirement(1, 
                                              requirement.total_credit,
                                              isFrom,
                                              requirement.minimum_grade,
                                              requirement.required_average)

        if requirement.is_admission:            
            result.admission_requirements.append(resultRequirement)
        else:
            result.module_requirements.append(resultRequirement)

        for course in requirement.courses: 
            
            resultCourse = ResultCourse(None,
                                        None,
                                        course.subject_name,
                                        course.number,
                                        course.suffix)
            
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
                
                elif tempCourse[1] == 'F' or tempCourse[1] == 'WDN' or tempCourse[1] == 'RNC':
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

    return result