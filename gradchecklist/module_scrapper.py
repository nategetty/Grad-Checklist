import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .module import Module, insert_module, ModuleRequirement, ModuleRequirementSubject, get_module
from .course import get_v_course_by_name
from .subject import get_subject_by_name
from .db import create_db_connection

db = create_db_connection()

# Function to get all the links from the intial website
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    target = soup.find('div', {'id': "AdmissionRequirements"}) #first year requirements
    target1 = soup.find('div', class_="moduleInfo") #module requirements

    if target:
        links += [urljoin(url, a['href']) for a in target.find_all('a', href=True)]
    if target1:
        links += links + [urljoin(url, a['href']) for a in target1.find_all('a', href=True)]
    else:
        return []

    return links

#Function to fetch the html from the original url
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch URL: {url}")
        return None

# Main function to initiate the scraping process
def main():
    course_name = ""
    course_code=""
    course_amount = None
    admissionCourses = []
    moduleCourses = []
    moduleReq = []
    admissionReq = []
    subjectCourses = []
    minimumgrade = ""
    course_weight = 0
    skip=False
    first = True
    pattern = re.compile(r'(\w+\s\d{4}[A-Z]\/[A-Z])')
    pattern2 = r'with a mark of at least (\d+)%'
    base_url = "https://www.westerncalendar.uwo.ca/"
    url = 'https://www.westerncalendar.uwo.ca/Departments.cfm?DepartmentID=62&SelectedCalendar=Live&ArchiveID='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('div', class_="panel panel-default")

    if table:
        links = table.find_all('a')
        links = links[1:]

        for link_info in links:
            link = link_info['href']
            #link = 'https://www.westerncalendar.uwo.ca/Modules.cfm?ModuleID=21118&SelectedCalendar=Live&ArchiveID='
            module_link = urljoin(base_url, link)

            module_response = requests.get(module_link)
            module_soup = BeautifulSoup(module_response.text, 'html.parser')

            elements = module_soup.find('h2')

            for element in elements:
                element = element.get_text().strip()
                if element.isupper():
                    moduleName = element
                    print(moduleName)



            admissionRequirements = module_soup.find(id= "AdmissionRequirements")
            admissionGradeRequirements = admissionRequirements.get_text().strip().split('\n')[0]
            #print(admissionRequirements.get_text().strip().split('\n')[0])

            modulesAdmission = admissionRequirements.find_all('div')

            if modulesAdmission == []:
                if admissionRequirements.find('a'):
                    modulesAdmission = admissionRequirements.find('a')
                    course_text = modulesAdmission.get_text().strip(",")
                    course_text = course_text.strip(" or ")
                    match = re.match(r'(.+?) (\d{4}[A-Z]?)(?:A/B)?$', course_text)
                    if match:
                        course_name = match.group(1)
                        course_code = match.group(2)
                        course_code = course_code[:4]

                        currCourse = get_v_course_by_name(db, course_name, course_code)
                        #print(currCourse)

                        admissionCourses.append(currCourse)

            for module in modulesAdmission:
                spanText = module.get_text()

                '''if first == True:
                    print(spanText)
                    first = False'''
                if module.find('strong'):
                    skip = True
                    pass
                elif skip == True:
                    pass
                elif 'course' in spanText:
                    #need to take a credit amount to get
                    match2 = re.search(pattern2, spanText)
                    course_amount = spanText[0:3]
                    #print("COURSE" + course_amount)
                    courses = module.find_all('a')
                    #print(module)
                    for course in courses:
                        course_text = course.get_text().strip(",")
                        course_text = course_text.strip(" or ")
                        match = re.match(r'(.+?) (\d{4}[A-Z]?)(?:A/B)?$', course_text)
                        if match:
                            course_name = match.group(1)
                            course_code = match.group(2)
                            course_code = course_code[:4]

                            currCourse = get_v_course_by_name(db, course_name, course_code)
                            #print(currCourse)

                            admissionCourses.append(currCourse)

                            #print(course_name)
                            #print(course_code)

                    if match2: #has the minimum grade
                        minimumgrade = match2.group(1)
                        #print(minimumgrade)
                    #print(course_amount)
                    #print(module)
                elif 'and' in spanText and "Note" not in spanText and 'course' not in spanText:
                    #each course will be 0.5 and added as its own admission module requirement
                    courses = module.find_all('a')
                    #print(courses)
                    for course in courses:
                        course_text = course.get_text().strip(",")
                        course_text = course_text.strip(" or ")

                        match = re.match(r'(.+?) (\d{4}[A-Z]?)(?:A/B)?$', course_text)
                        if match:
                            course_name = match.group(1)
                            course_code = match.group(2)
                            course_code = course_code[:4]

                            currCourse = get_v_course_by_name(db, course_name, course_code)
                            course_weight += currCourse.credit
                            course_amount = course_weight
                            #print(currCourse)

                            admissionCourses.append(currCourse)

                            #print(course_name)
                            #print(course_code)

                elif 'at least' in spanText:
                    #print("AR LEAST")
                    #has a minimum grade
                    #print(spanText)
                    match2 = re.search(pattern2, spanText)
                    courses = module.find_all('a')
                    course_amount=0.5
                    for course in courses:
                        course_text = course.get_text().strip(",")
                        course_text = course_text.strip(" or ")
                        match = re.match(r'(.+?) (\d{4}[A-Z]?)(?:A/B)?$', course_text)
                        if match:
                            course_name = match.group(1)
                            course_code = match.group(2)
                            course_code = course_code[:4]

                            currCourse = get_v_course_by_name(db, course_name, course_code)
                            #print(currCourse)

                            admissionCourses.append(currCourse)

                            #print(course_name)
                            #print(course_code)

                        if match2:
                            minimumgrade = match2.group(1)
                            #print(minimumgrade)


            #print(modulesAdmission)

                if minimumgrade == '':
                    #print(course_amount)
                    currModuleRequirement = ModuleRequirement(id=0, module_id=0, total_credit=course_amount, minimum_grade=None, is_admission=True, courses=admissionCourses, subjects=subjectCourses)
                    admissionReq.append(currModuleRequirement)
                elif skip == False:
                    #print(course_amount)
                    currModuleRequirement = ModuleRequirement(id=0, module_id=0, total_credit=course_amount, minimum_grade=minimumgrade, is_admission=True, courses=admissionCourses, subjects=subjectCourses)
                    admissionReq.append(currModuleRequirement)
                #print(currModuleRequirement)
                #print("\n")
                admissionCourses = []
                minimumgrade = ""
                course_weight = ""


            print("\n")
            skip = False
            first = True
            break_ = False

            #admissionReq = []
            minimumgrade = ''
            course_weight = ''



            moduleRequirements = module_soup.find(class_= "moduleInfo")
            if moduleRequirements.find_all('p')[1].find('a'):
                moduleRequirements = moduleRequirements.find_all('p')[1]
            else:
                moduleRequirements = moduleRequirements.find_all('p')[2]
            #print(moduleRequirements)
            #courseValues = moduleRequirements.find_all('strong')


            strong_tags = moduleRequirements.find_all('strong')
            for index, strong_tag in enumerate(strong_tags):
                moduleCourses = []
                subjectCourses = []
                value = strong_tag.text.strip()  # Extract the text within <strong> tags
                # Find the next sibling element after the <strong> tag
                course_weight = value[:3]

                next_sibling = strong_tag.next_sibling
                while next_sibling is not None and next_sibling.name != 'strong':
                    if '*' in next_sibling.get_text() and len(strong_tags)-1==index:
                        break;
                    if next_sibling.name == 'a':  # Check if the sibling is an <a> tag
                        #print(next_sibling)
                        information = next_sibling.get_text(strip=True)  # Extract the text content of the <a> tag
                        information = information.strip(",")
                        information = information.strip(".")

                        match = re.match(r'(.+?) (\d{4}[A-Z]?)(?:/[A-Z]?(?:/[A-Z]?)?)?$', information)

                        if match:
                            courseName = match.group(1)
                            courseCode = match.group(2)
                            courseCode = courseCode[:4]
                            #print(courseName)
                            #print(courseCode)

                            currCourse = get_v_course_by_name(db, courseName, courseCode)

                            moduleCourses.append(currCourse)
                            #print("HELLP" + currCourse.subject_name)
                            #print(currCourse.subject_code)


                    if callable(next_sibling.strip):  # Check if the strip() method is callable
                        information = next_sibling.strip()  # Extract the text content
                        parts = information.split(" at the ")
                        if len(parts) == 2:
                            subject = parts[0].strip().replace(" courses", "").strip()
                            subject = subject.replace(" from: ", "").strip()
                            subject = subject.replace("from: ", "").strip()
                            level_info = parts[1].split()[0]
                            #print(level_info)

                            if '-' in level_info:
                                level_parts = level_info.split('-')
                                level = ''.join(filter(str.isdigit, level_parts[0]))  # Extract the digits
                            else:
                                level = ''.join(filter(str.isdigit, level_info))  # Extract the digits


                            #print("Subject:", subject)
                            if subject != ';':
                                #moduleCourses.append((subject, level, "YES"))

                                check = get_subject_by_name(db, subject)
                                if check == None:
                                    print("CHECK1" + subject)

                                currModuleRequirement = ModuleRequirementSubject(check.code, level)

                                subjectCourses.append(currModuleRequirement)


                        #print("TEST: " +  information)

                        pattern = r'from:\s*([\w\s]+?)\s+courses?\s+at\s+the\s+(\d{4})-?level\s+or\s+above'

                        matches2 = re.findall(pattern, next_sibling.get_text())

                        if matches2:
                            subject = matches2[0][0]
                            level = matches2[0][1]

                            check = get_subject_by_name(db, subject)
                            if check == None:
                                print("CHECK2" + subject)

                            currModuleRequirement = ModuleRequirementSubject(check.code, level)
                            subjectCourses.append(currModuleRequirement)

                            #moduleCourses.append((subject.strip(), level, "YES"))

                        matches = re.findall(r'(?:courses\s+at\s+the\s+(\d{4})\s*level\s+or\s+above|courses\s+numbered\s+(\d{4})\s*or\s+above)\s+in\s+([\w\s,]+)', next_sibling.get_text())
                        for match in matches:
                            level = match[0] if match [0] else match[1]
                            subjects = match[2].split(',')
                            for subject in subjects:
                                if (level.isdigit()):
                                    subject = subject.lstrip()
                                    print(subject)
                                    check = get_subject_by_name(db, subject)
                                    #print(subject[1:])
                                    if check == None:
                                        print("CHECK3" + subject)
                                    currModuleRequirement = ModuleRequirementSubject(check.code, level)
                                    subjectCourses.append(currModuleRequirement)
                                    #moduleCourses.append((subject.strip(), level, "YES"))

                        pattern = r'numbered\s+(\d{4})\s+or\s+higher\s+in\s+([\w\s,]+)'
                        matches3 = re.findall(pattern, next_sibling.get_text())

                        if matches3:
                            for match in matches3:
                                level = match[0]
                                subjects = match[1].split(', ')
                                for subject in subjects:
                                    #moduleCourses.append((subject.strip(), level, "YES"))

                                    check = get_subject_by_name(db, subject)
                                    if check == None:
                                        pass
                                        print("CHECK4" + subject)
                                    else:
                                        currModuleRequirement = ModuleRequirementSubject(check.code, level)
                                        subjectCourses.append(currModuleRequirement)




                        '''if information.endswith("."):
                            parts = information.split(" courses")
                            if len(parts) == 2:
                                subject = parts[0].strip().replace(" courses", "").strip()
                                subject = subject.replace(" from: ", "").strip()
                                level_info = parts[1]
                                level = ''.join(filter(str.isdigit, level_info))

                                #print("Subject:", subject)
                                #print("Level:", level)
                                moduleCourses.append((subject, level, "YES"))'''



                    next_sibling = next_sibling.next_sibling  # Move to the next sibling


                #moduleReq.append((moduleName, course_weight, moduleCourses))
                if course_weight != ":":
                    if minimumgrade == '':
                        #print(course_weight)
                        currModuleRequirement = ModuleRequirement(id=0, module_id=0, total_credit=course_weight, minimum_grade=None, is_admission=False, courses=moduleCourses, subjects=subjectCourses)
                        moduleReq.append(currModuleRequirement)
                    else:
                        #print(course_weight)
                        currModuleRequirement = ModuleRequirement(id=0, module_id=0, total_credit=course_weight, minimum_grade=minimumgrade, is_admission=False, courses=moduleCourses, subjects=subjectCourses)
                        moduleReq.append(currModuleRequirement)


                    #print(currModuleRequirement.id)
                    print("\n")

                #moduleReq = [

            requirements = []

            for admission in admissionReq:
                if admission.courses!=[]:
                    requirements.append(admission)

            for module in moduleReq:
                if module.courses!=[]:
                    requirements.append(module)
                    #print(module)


            try:
                currModule = Module(id = 0, name=moduleName, requirements=requirements)
                print(moduleName)
                #print(currModule)
                insert_module(db, currModule)
                print(get_module(db, moduleName))
                #print(currModule)
            except Exception as e:
                print(e)
            print("TESTING")
            print(get_module(db, moduleName))






            admissionReq=[]
            moduleReq = []




if __name__ == "__main__":
    main()
