import re
from .student import Student

class CourseScrapper:

    def filterLines(text, values):

        lines = text.split('\n')
        pattern = re.compile(f'^({"|".join(map(re.escape, values))})')
        filteredLines = []

        for line in lines:
            line = re.sub(r'\.\.\..*$', '', line)
            if pattern.match(line):
                filteredLines.append(line)

        return filteredLines

    def extractCourseInfo(line):

        subjectCode = re.match(r'^([A-Z]+)', line).group(1)

        courseCodeMatch = re.search(r'(\d{4}[A-Z]?)', line)
        courseCode = courseCodeMatch.group(1) if courseCodeMatch else None

        # gradeMatch = re.search(r'(\d{3}|SPC|WDN|F)', line[::-1])
        # grade = gradeMatch.group(1)[::-1] if gradeMatch and gradeMatch.group(1) in ('SPC', 'WDN', 'F') or 0 <= int(gradeMatch.group(1)[::-1]) <= 100 else "N\/A"
        gradeMatch = re.search(r'(\d{3}|SPC|WDN|F)', line.rsplit(" ", 1)[-1])
        if gradeMatch is not None:
            grade = gradeMatch.group(1)
        else:
            grade = None

        rncMatch = re.search(r'(RNC)', line)
        if rncMatch and rncMatch.group(1) == 'RNC':
            return None

        if line.endswith("WDN") or line.endswith("SPC") or line.endswith("PAS"):
            grade = line.split()[-1]

        return {
            'subjectCode': subjectCode,
            'courseCode': courseCode,
            'grade': grade
        }
