import requests
from bs4 import BeautifulSoup
from .subject import Subject, insert_subject
from .db import create_db_connection

db = create_db_connection()

# Function to get all the links from the intial website
def get_subjects(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    course_breadth2 = "null"

    courses = soup.find("table").find_all('tr')

    for index, course in enumerate(courses):
        if (index !=0 ):
            link = course.find('a')
            course_name_breadth = course.getText(strip=True)
            cat_index = course_name_breadth.find("CATEGORY")
            course_name = course_name_breadth[:cat_index].strip()
            course_breadth = course_name_breadth[cat_index + len("CATEGORY"):].strip()

            if cat_index == -1:
                course_breadth = "null"
                course_breadth2 = "null"

            elif len(course_breadth)>1:
                cat_index = course_breadth.find("CATEGORY")
                course_breadth2 = course_breadth[cat_index + len("CATEGORY"):].strip()
                course_breadth = course_breadth[0]

            if link != None:
                href_val = link['href']
                if href_val!=None:
                    subject_value = href_val.split('Subject=')[1].split('&')[0]
                    #print(subject_value)
            print(course_name_breadth)
            print(course_breadth)
            print(course_breadth2)


            try:
                if (course_breadth=="null"):
                    subject = Subject(subject_value, course_name)
                    insert_subject(db, subject)
                elif (course_breadth2=="null"):
                    subject = Subject(subject_value, course_name, course_breadth)
                    insert_subject(db, subject)
                else:
                    subject = Subject(subject_value, course_name, course_breadth, course_breadth2)
                    insert_subject(db, subject)

            except Exception as e:
                print(e)

            course_breadth2="null"



# Main function to initiate the scraping process
def main():
    url = 'https://www.westerncalendar.uwo.ca/Courses.cfm?SelectedCalendar=Live&ArchiveID='
    get_subjects(url)


if __name__ == "__main__":
    main()
