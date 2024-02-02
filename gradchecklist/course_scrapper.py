import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .course import Course, insert_course
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

#Function to fetch the information from html
def fetch_info(html):
    stripped_course_weight = "Null"
    stripped_breadth = "Null"
    stripped_subject = "Null"
    nameAndNumber = "Null"
    properName = "Null"
    prerequisites = "Null"
    antirequisites = "Null"
    desciption = "Null"
    extraInformation = "Null"
    courseCode = "Null"
    suffix = "Null"
    found = 0;
    soup = BeautifulSoup(html, 'html.parser')
    courseNames = soup.find("div", class_="col-md-12") #to find anti/pre/corequistes and extra information
    results  = soup.find_all("div", class_="col-xs-12") #to find the names of the courses
    pattern = re.compile(r'(\d+)(([A-Z]/[A-Z])|[A-Z])')

    if courseNames:
        nameAndNumber = courseNames.find("h2").get_text(strip=True)
        match = pattern.search(nameAndNumber)

        if match:
            courseCode = match.group(1)
            suffix = match.group(2)

        properName = courseNames.find("h3").get_text(strip=True)

    for result in results:
        if not (result.find('label')): #if there is not label it is the extra info (weight, breadth and subject code)
            courseInfo = result.find_all("h5")
            if courseInfo: #parsing all extra information
                course_weight = courseInfo[0].get_text(strip=True)
                stripped_course_weight = course_weight.split(":")[1].strip(' "==$')
                breadth = courseInfo[1].get_text(strip=True)
                stripped_breadth = breadth.split("CATEGORY ", 1)[1].strip('i')
                subject = courseInfo[2].get_text(strip=True)
                stripped_subject = subject.split(":",1)[1]


        elif (result.find("label", {"for": "Antirequisites"})): #finding the antirequistes (not sure how to parse them yet)
            antirequisites =  result.getText(strip=True)

        elif(result.find("div").find("strong", string="Prerequisite(s):")): #finding the pre/corequisites (not sure hot to parse them yet)
            prerequisites = result.getText(strip=True)

        elif (result.find('label', {'for': 'CourseDescription', 'class': 'novecentoMedium borderBottom'}) and found==0):
            desciption = result.getText(strip=True)
            found = 1

        elif (result.find("div").find('strong', string="Extra Information:")):
            extraInformation = result.getText(strip = True).replace('Extra InformationExtra Information:', "", 2)



    #print the findings (will store it in a database soon)
    try:
        course = Course(0, stripped_subject, int(courseCode), suffix, properName, desciption, extraInformation)
        insert_course(db, course)
    except Exception as e:
        print (e)
        pass

    '''print(nameAndNumber)
    print(courseCode)
    print(suffix)
    print(properName)
    print (desciption)
    print(prerequisites)
    print(antirequisites)
    print(stripped_course_weight)
    print(stripped_breadth)
    print(stripped_subject)
    print(extraInformation)'''


# Main function to initiate the scraping process
def main():
    # Replace 'your_url_here' with the actual URL you want to scrape
    url = 'https://www.westerncalendar.uwo.ca/Modules.cfm?ModuleID=21123&SelectedCalendar=Live&ArchiveID='
    html_content = fetch_html(url)

    if html_content: #if fetching is successful
        links = get_links(url)

        for link in links: #parse all the links found
            print(link)
            link_html_content = fetch_html(link)
            fetch_info(link_html_content)


if __name__ == "__main__":
    main()
