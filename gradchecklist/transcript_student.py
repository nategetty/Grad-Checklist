import re

class StudentScrapper:
    def extract_student_info(text):
        
        studentNumMatch = re.search(r'\b(\d{9})\b', text)
        studentNumber = studentNumMatch.group(1) if studentNumMatch else None

        nameMatch = re.search(r'Primary Name: (\w+), (\w+)', text)
        lastName = nameMatch.group(1) if nameMatch else None
        firstName = nameMatch.group(2) if nameMatch else None

        return {
            'studentNumber': studentNumber,
            'lastName': lastName,
            'firstName': firstName
        }
