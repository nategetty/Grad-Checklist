from .student import Student
from .transcript_course import CourseScrapper
from .module import get_module
from .subject import get_all_subject_codes
from .db import get_db
import PyPDF2 as pypdf
import re

def extractTextFromPDF(pdfReader):
    text = ''
    for pageNum in range(len(pdfReader.pages)):
        page = pdfReader.pages[pageNum]
        text += page.extract_text()
    return text

def extractStudentInfo(text):
    studentNumMatch = re.search(r'\b(\d{9})\b', text)
    studentNumber = studentNumMatch.group(1) if studentNumMatch else None

    nameMatch = re.search(r'Primary Name: (\w+), (\w+)', text)
    lastName = nameMatch.group(1) if nameMatch else None
    firstName = nameMatch.group(2) if nameMatch else None

    return Student(
                  studentNumber=studentNumber, 
                  lastName=lastName, 
                  firstName=firstName
                  )

def extractITR(db, pageText, student):
    lines = pageText.split('\n')
    for line in lines:
        plan_match = re.search(r'Plan:(.+)', line)
        if plan_match:
            plan = plan_match.group(1)
            module = None
            if any(tag in plan for tag in ["HSP", "SP", "MAJ", "MIN"]):
                if "HSP" in plan:
                    module = get_module(db, "HONOURS SPECIALIZATION IN COMPUTER SCIENCE")
                elif "SP" in plan:
                    module = get_module(db, "SPECIALIZATION IN COMPUTER SCIENCE")
                elif "MAJ" in plan:
                    module = get_module(db, "MAJOR IN COMPUTER SCIENCE")
                elif "MIN" in plan:
                    if "Software Engineering" in plan:
                        module = get_module(db, "MINOR IN SOFTWARE ENGINEERING")
                    elif "Game Development" in plan:
                        module = get_module(db, "MINOR IN GAME DEVELOPMENT")
                    else:
                        module = get_module(db, "MINOR IN COMPUTER SCIENCE")
                if module:
                    if len(student.itr) < 2:
                        student.itr.append(module)
                    elif any(tag in module.name for tag in ["SPECIALIZATION", "MAJOR"]):
                        student.itr[0] = module
                    elif "MINOR" in module.name:
                        student.itr[1] = module

def processTranscript(fileObject):
    db = get_db()
    subjectCodes = get_all_subject_codes(db)
    pdfReader = pypdf.PdfReader(fileObject)
    students = []

    for _ in range(len(pdfReader.pages)):
        pageText = extractTextFromPDF(pdfReader)

        student = extractStudentInfo(pageText)

        if student.studentNumber not in [stdnt.studentNumber for stdnt in students]:
            students.append(student)

        extractITR(db, pageText, student)

        filteredLines = CourseScrapper.filterLines(pageText, subjectCodes)

        for line in filteredLines:
            courseInfo = CourseScrapper.extractCourseInfo(line)
            if courseInfo is not None:
                student.addCourse(db, courseInfo['courseCode'], courseInfo['subjectCode'], courseInfo['grade'])

    return students

if __name__ == "__main__":
    processTranscript()
