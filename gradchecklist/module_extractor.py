from functools import reduce
from bs4 import BeautifulSoup
from requests import get
from decimal import Decimal
from .db import create_db_connection
from .course import VCourse, get_v_course
from .module import Module, ModuleRequirement, insert_module
import re
import json

def main():
    db = create_db_connection()
    url = "https://www.westerncalendar.uwo.ca/Modules.cfm?SelectedCalendar=Live&ArchiveID="
    page = get(url)

    content = page.content.decode("utf-8")
    soup = BeautifulSoup(content, 'html.parser')
    rows = soup.find_all('tr')

    links_list = []

    for row in rows:
        if row.text.strip().startswith("COMPUTER SCIENCE"):
            cols = row.find_all('td')

            links_td = cols[3]
            links = links_td.find_all('a')

            file = open("modules.txt", "w")

            for link in links:
                link_href = link.get('href')
                link_href = str(link_href).removeprefix(".")
                links_list.append("https://www.westerncalendar.uwo.ca" + link_href)
                file.write("https://www.westerncalendar.uwo.ca" + link_href + '\n')
            file.close()

    with (open("modules.txt", "r") as src):
        for line in src:
            site = line.strip()
            # print(src.readline().strip())             URL link
            page = get(site)
            # print(page)                               Status of link

            content = page.content.decode("utf-8")
            soup = BeautifulSoup(content, 'html.parser')

            title = soup.find_all('h2')
            for element in title:
                element.small.decompose()
            print(title[0].text.strip())

            print('\n')
            print(f'Admission Info:')
            admin_sect = soup.find_all('div', class_='admInfo')
            adm_text = ""
            for admin_line in admin_sect:
                adm_text += admin_line.text.strip()
            adm_req = re.split(': |, |\. |(?<=\D)\.(?=\d)|; |\n', adm_text)
            replacements = ['\xa0', 'the former ', ' from', 'from', ' courses', ' course']
            adm_req = [reduce(lambda item, rp: item.replace(rp, ''), replacements, item) for item in adm_req]

            adm_req = [item.replace('Computer Science', 'COMPSCI') for item in adm_req]
            adm_req = [item.replace('Statistical Sciences', 'STATS') for item in adm_req]
            adm_req = [item.replace('Biology', 'BIOLOGY') for item in adm_req]
            adm_req = [item.replace('Data Science', 'DATASCI') for item in adm_req]
            adm_req = [item.replace('Engineering Science', 'ENGSCI') for item in adm_req]
            adm_req = [item.replace('Science', 'SCIENCE') for item in adm_req]
            adm_req = [item.replace('Writing', 'WRITING') for item in adm_req]
            adm_req = [item.replace('Applied Mathematics', 'APPLMATH') for item in adm_req]
            adm_req = [item.replace('Calculus', 'CALC') for item in adm_req]
            adm_req = [item.replace('Numerical and Mathematical Methods', 'NMM') for item in adm_req]
            adm_req = [item.replace('Mathematics', 'MATH') for item in adm_req]

            temp_list = []
            for item in adm_req:
                if 'or' in item and not item.endswith('or above'):
                    split_items = [i.strip() for i in item.split('or')]
                    temp_list.extend(split_items)
                else:
                    temp_list.append(item)
            adm_req = temp_list
            adm_req = [item for item in adm_req if item.strip()]

            if 'Note' in adm_req:
                adm_req = adm_req[:adm_req.index('Note')]
            start_index = next((index for index, value in enumerate(adm_req) if value[0].isdigit()), None)
            if start_index is not None:
                adm_req = adm_req[start_index:]

            # print(adm_text)
            # print(adm_req)

            reqs = []
            set_list = []
            credit_list = []
            minimum_grade = []
            for element in adm_req:
                if element[0].isdigit():
                    if set_list:
                        reqs.append(set_list)
                    set_list = []
                    credit_list.append(element)
                else:
                    set_list.append(element)
            if set_list:
                reqs.append(set_list)
            print(reqs)
            print(credit_list)

            mod_req_list = []
            for i, req in enumerate(reqs):
                minimum_flag = False
                for j, _ in enumerate(req):
                    minimum = re.search(r'(\d{2})%', req[j])
                    if minimum:
                        minimum_grade.append(minimum.group(1))
                        minimum_flag = True
                if not minimum_flag:
                    minimum_grade.append(None)
            print(minimum_grade)

            mod_req_list.append(ModuleRequirement(
                total_credit=Decimal(credit_list[i]),
                is_admission=True,
                minimum_grade=minimum_grade[i],
                courses=[
                    get_v_course(db,
                                 course.split()[0],
                                 int(course.split()[3]) if 'level' in course.split() else int(course.split()[1][:4]))
                    for course in req
                ]
            ))

            print('\n')
            print(f'Module Info:')
            module_sect = soup.find_all('div', class_='moduleInfo')
            mod_text = ""
            for module_line in module_sect:
                mod_text += module_line.text.strip()
            mod_req = re.split(': |:|, |\. |(?<=\D)\.(?=\d)|\n', mod_text)
            replacements = ['\xa0', 'the former ', ' from', 'from', ' courses', ' course']
            mod_req = [reduce(lambda item, rp: item.replace(rp, ''), replacements, item) for item in mod_req]
            mod_req = [item.replace('Computer Science', 'COMPSCI') for item in mod_req]
            mod_req = [item.replace('Statistical Sciences', 'STATS') for item in mod_req]
            mod_req = [item.replace('Biology', 'BIOLOGY') for item in mod_req]
            mod_req = [item.replace('Data Science', 'DATASCI') for item in mod_req]
            mod_req = [item.replace('Engineering Science', 'ENGSCI') for item in mod_req]
            mod_req = [item.replace('Science', 'SCIENCE') for item in mod_req]
            mod_req = [item.replace('Writing', 'WRITING') for item in mod_req]
            mod_req = [item.replace('Applied Mathematics', 'APPLMATH') for item in mod_req]
            mod_req = [item.replace('Calculus', 'CALC') for item in mod_req]
            mod_req = [item.replace('Numerical and Mathematical Methods', 'NMM') for item in mod_req]
            mod_req = [item.replace('Mathematics', 'MATH') for item in mod_req]

            temp_list = []
            for item in mod_req:
                if 'or' in item and not item.endswith('or above'):
                    split_items = [i.strip() for i in item.split('or')]
                    temp_list.extend(split_items)
                else:
                    temp_list.append(item)
            mod_req = temp_list
            mod_req = [item for item in mod_req if item.strip()]

            if 'Note' in mod_req:
                mod_req = mod_req[:mod_req.index('Note')]
            start_index = next((index for index, value in enumerate(mod_req) if value[0].isdigit()), None)
            if start_index is not None:
                mod_req = mod_req[start_index:]
            # print(mod_text)
            # print(mod_req)

            reqs = []
            set_list = []
            credit_list = []
            minimum_grade = []
            for element in mod_req:
                if element[0].isdigit():
                    if set_list:
                        reqs.append(set_list)
                    set_list = []
                    credit_list.append(element)
                else:
                    set_list.append(element)
            if set_list:
                reqs.append(set_list)
            print(reqs)
            print(credit_list)

            for i, req in enumerate(reqs):
                minimum_flag = False
                for j, _ in enumerate(req):
                    minimum = re.search(r'(\d{2})%', req[j])
                    if minimum:
                        minimum_grade.append(minimum.group(1))
                        minimum_flag = True
                if not minimum_flag:
                    minimum_grade.append(None)
            print(minimum_grade)

            mod_req_list.append(ModuleRequirement(
                total_credit=Decimal(credit_list[i]),
                is_admission=False,
                minimum_grade=minimum_grade[i],
                courses=[
                    get_v_course(db,
                                 course.split()[0],
                                 int(course.split()[3]) if 'level' in course.split() else int(course.split()[1][:4]))
                    for course in req
                ]
            ))

            module = Module(name=title[0].text.strip(), requirements=mod_req_list)
            # insert_module(db, module)
            print('\n')


if __name__ == "__main__":
    main()
