from .student import Student
from .transcript_course import CourseScrapper
from .transcript_student import StudentScrapper
from .db import get_db
import PyPDF2

def extract_text_from_pdf(file_object):
    pdf_reader = PyPDF2.PdfReader(file_object)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def main(file_object):

    db = get_db()

    pdf_text = extract_text_from_pdf(file_object)
    studentInfo = StudentScrapper.extract_student_info(pdf_text)

    student = Student(
         studentNumber=studentInfo['studentNumber'], 
         lastName=studentInfo['lastName'], 
         firstName=studentInfo['firstName'])

    values_to_find = ['ACTURSCI', 'ASL', 'AMERICAN', 'ADS', 'ANATCELL', 'ANTHRO', 'APPLMATH', 'ARABIC', 'AH', 'AISE', 'ARTHUM', 'ASTRONOM', 'BIBLSTUD', 'BIOCHEM', 'BIOLOGY', 'BME', 'BIOSTATS', 'BUSINESS', 
                      'CALCULUS', 'CGS', 'CBE', 'CHEMBIO', 'CHEM', 'CYS', 'CHINESE', 'CHURCH', 'CHURLAW', 'CHURMUSI', 'CEE', 'CLASSICS', 'COMMSCI', 'COMPLIT', 'COMPSCI', 'CA', 'DANCE', 'DATASCI', 'DIGICOMM', 
                      'DIGIHUM', 'DISABST', 'EARTHSCI', 'ECONOMIC', 'EDUC', 'ECE', 'ELI', 'ENGSCI', 'ENGLISH', 'ENVIRSCI', 'EPID', 'EPIDEMIO', 'FIMS', 'FAMLYSTU', 'FLDEDUC', 'FILM', 'FINMOD', 'FOODNUTR', 
                      'FRENCH', 'GSWS', 'GEOGRAPH', 'GERMAN', 'GGB', 'GLE', 'GREEK', 'GPE', 'HEALTSCI', 'HEBREW', 'HISTTHEO', 'HISTORY', 'HISTSCI', 'HOMILET', 'HUMANECO', 'HUMANRS', 'INDIGSTU', 'IE', 'INTEGSCI', 
                      'INTERDIS', 'INTREL', 'ITALIAN', 'JAPANESE', 'JEWISH', 'KINESIOL', 'LATIN', 'LAW', 'LS', 'LINGUIST', 'LITURST', 'LITURGIC', 'MOS', 'MATH', 'MME', 'MSE', 'MIT', 'MBI', 'MEDBIO', 'MEDSCIEN', 
                      'MEDIEVAL', 'MICROIMM', 'MORALTHE', 'MCS', 'MUSIC', 'NEURO', 'NMM', 'NURSING', 'ONEHEALT', 'PASTTHEO', 'PATHOL', 'PHARM', 'PHILST', 'PHILOSOP', 'PHYSICS', 'PHYSIOL', 'PHYSPHRM', 'POLISCI', 
                      'PPE', 'PSYCHOL', 'REHABSCI', 'RELEDUC', 'RELSTUD', 'SACRTHEO', 'SCHOLARS', 'SCIENCE', 'SOCLJUST', 'SOCWORK', 'SOCIOLOG', 'SE', 'SPANISH', 'SPEECH', 'SPIRTHEO', 'STATS', 'SA', 'SUPPAST', 
                      'SYSTHEO', 'THANAT', 'TNLA', 'THEATRE', 'THEOETH', 'THEOLST', 'THESIS', 'TJ', 'WRITING']
    
    filtered_lines = CourseScrapper.filter_lines(pdf_text, values_to_find)

    for line in filtered_lines:
        
        courseInfo = CourseScrapper.extract_course_info(line)
        if courseInfo is not None:
            student.add_course(db, courseInfo['courseCode'], courseInfo['subjectCode'], courseInfo['grade'])
            
    return student

if __name__ == "__main__":
    main()