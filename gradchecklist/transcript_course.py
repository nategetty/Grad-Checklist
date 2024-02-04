import re
from .student import Student

class CourseScrapper:

    def filter_lines(text, values):

        lines = text.split('\n')
        pattern = re.compile(f'^({"|".join(map(re.escape, values))})')
        filtered_lines = []

        for line in lines:
            line = re.sub(r'\.\.\..*$', '', line)
            if pattern.match(line):
                filtered_lines.append(line)

        return filtered_lines

    def extract_course_info(line):

        subjectCode = re.match(r'^([A-Z]+)', line).group(1)

        course_code_match = re.search(r'(\d{4}[A-Z]?)', line)
        courseCode = course_code_match.group(1) if course_code_match else None

        grade_match = re.search(r'(\d{3}|SPC|WDN|F)', line[::-1])
        grade = grade_match.group(1)[::-1] if grade_match and grade_match.group(1) in ('SPC', 'WDN', 'F') or 0 <= int(grade_match.group(1)[::-1]) <= 100 else "N\/A"

        rnc_match = re.search(r'(RNC)', line)
        if rnc_match and rnc_match.group(1) == 'RNC':
            return None

        if line.endswith("WDN") or line.endswith("SPC") or line.endswith("PAS"):
            grade = line.split()[-1]

        return {
            'subjectCode': subjectCode,
            'courseCode': courseCode,
            'grade': grade
        }
