from .course import get_v_course

class Student:
    def __init__(self, studentNumber, lastName, firstName):
        self.studentNumber = studentNumber
        self.lastName = lastName
        self.firstName = firstName
        self.courses = []
        self.itr = ["Major", "Minor"]

    def addCourse(self, db, courseCode, subjectCode, grade):
        self.courses.append((get_v_course(db, subjectCode, courseCode), grade))

    def __str__(self):
        return f"Student: {self.firstName} {self.lastName} ({self.studentNumber}), Courses: {len(self.courses)}, ITR: {self.itr}"        