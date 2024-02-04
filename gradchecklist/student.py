from .course import get_v_course

class Student:
    def __init__(self, studentNumber, lastName, firstName):
        self.studentNumber = studentNumber
        self.lastName = lastName
        self.firstName = firstName
        self.courses = []

    def add_course(self, db, courseCode, subjectCode, grade):
        self.courses.append((get_v_course(db, subjectCode, courseCode), grade))
        

        