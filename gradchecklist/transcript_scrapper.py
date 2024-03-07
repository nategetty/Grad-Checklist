from .student import Student
from .transcript_course import CourseScrapper
from .db import get_db
import PyPDF2
import re

def extractTextFromPDF(fileObject):
    pdfReader = PyPDF2.PdfReader(fileObject)
    text = ''
    for pageNum in range(len(pdfReader.pages)):
        text += pdfReader.pages[pageNum].extract_text()
    return text

def extractStudentInfo(text):
    studentNumMatch = re.search(r'\b(\d{9})\b', text)
    studentNumber = studentNumMatch.group(1) if studentNumMatch else None

    nameMatch = re.search(r'Primary Name: (\w+), (\w+)', text)
    lastName = nameMatch.group(1) if nameMatch else None
    firstName = nameMatch.group(2) if nameMatch else None

    return Student(
                  studentNumber = studentNumber, 
                  lastName = lastName, 
                  firstName = firstName
                  )

def getSubjectCodes(db):
    with db.cursor() as c:
        c.execute("SELECT DISTINCT subject_code FROM VCourse")
        subjectCodes = c.fetchall()
    return subjectCodes

def processTranscript(fileObject):
    db = get_db()
    subjectCodes = getSubjectCodes(db)
    valuesToFind = [course[0] for course in subjectCodes]
    pdfReader = PyPDF2.PdfReader(fileObject)
    students = []

    for pageNum in range(len(pdfReader.pages)):
        pageText = extractTextFromPDF(fileObject)

        student = extractStudentInfo(pageText)

        if student.studentNumber not in [stdnt.studentNumber for stdnt in students]:
            students.append(student)
            
        filteredLines = CourseScrapper.filterLines(pageText, valuesToFind)

        for line in filteredLines:
            
            courseInfo = CourseScrapper.extractCourseInfo(line)
            if courseInfo is not None:
                student.addCourse(db, courseInfo['courseCode'], courseInfo['subjectCode'], courseInfo['grade'])

    return students

if __name__ == "__main__":
    processTranscript()