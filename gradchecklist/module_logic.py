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

    if not module.requirements:
        return result

    for student in students:
        
        result = createResult()

        for requirement in module.requirements:

            completedCount = Decimal(0)
            pendingCount = Decimal(0)

            minimumGrade = requirement.minimum_grade if requirement.minimum_grade is not None else 60

            courseSum = sum(course.credit for course in requirement.courses)

            isFrom = not requirement.total_credit == courseSum

            resultRequirement = ResultRequirement(
                1, 
                requirement.total_credit,
                isFrom,
                requirement.minimum_grade,
                requirement.required_average
            )

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

    # Calculate averages
    print("Admission Requirements:")
    for req in result.admission_requirements:
        print(f"Status: {req.status}, Total Credit: {req.total_credit}, Is From: {req.is_from}")
        print("Courses:")
        for course in req.courses:
            print(f"  Subject: {course.subject_name}, Number: {course.number}, Suffix: {course.suffix}, Grade: {course.grade}")

    # Printing module requirements
    print("\nModule Requirements:")
    for req in result.module_requirements:
        print(f"Status: {req.status}, Total Credit: {req.total_credit}, Is From: {req.is_from}")
        print("Courses:")
        for course in req.courses:
            print(f"  Subject: {course.subject_name}, Number: {course.number}, Suffix: {course.suffix}, Grade: {course.grade}")    
        
    return result
