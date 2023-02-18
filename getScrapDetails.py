import json
import logging
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
from mongodb import mongodbconnection
import mysql.connector

logging.basicConfig(filename="sg_logs.log", format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)

def all_course():
    try:
        ineuron_url = 'https://ineuron.ai/courses'
        uClient = uReq(ineuron_url)
        ineuron_page = uClient.read()
        uClient.close()
        ineuron_html = bs(ineuron_page, 'html.parser')
        course_data = json.loads(ineuron_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
        all_courses = course_data['props']['pageProps']['initialState']['init']['courses']
        course_namelist = list(all_courses.keys())
        return course_namelist
    except:
        logging.error('Error in scraping at all_course()')

### Function to Scrap one Course details from iNeuron website ###
def get_course_mysql(coursename):
    ineuron_url = 'https://ineuron.ai/course/'
    uClient = uReq(ineuron_url + str(coursename).replace(" ", "-"))
    course_page = uClient.read()
    uClient.close()
    ineuron_html = bs(course_page, 'html.parser')
    course_data1 = json.loads(ineuron_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
    logging.info('Get courses by title')
    all_dict = {}
    # list = []
    try:
        try:
            all_data = course_data1["props"]["pageProps"]
        except:
            all_data = 'No page'
        try:
            page_data = all_data['data']
        except:
            page_data = 'No data'
        try:
            detailed_data = page_data['details']
        except:
            detailed_data = 'No details'
        try:
            meta_data = page_data['meta']
        except:
            meta_data = 'No meta_data'
        try:
            curriculum_data = meta_data['curriculum']
        except:
            curriculum_data = 'No curriculum_data'
        try:
            overview_data = meta_data['overview']
        except:
            overview_data = 'No overview_data'
        # Building a Course Dictionary
        try:
            pricing_inr = detailed_data['pricing']['IN']
        except:
            pricing_inr = 'NULL'
        try:
            course_name = page_data['title']
        except:
            course_name = 'Name NA'
        try:
            description = detailed_data['description']
        except:
            description = "NULL"
        try:
            language = overview_data['language']
        except:
            language = 'NULL'
        try:
            req = overview_data['requirements']
        except:
            req = 'NULL'
        try:
            learn = overview_data['learn']
        except:
            learn = 'NULL'
        curriculum = []
        try:
            for i in curriculum_data:
                curriculum.append(curriculum_data[i]["title"])
            all_dict = {"Course_title": course_name, "Description": description,
                        "Language": language, "Pricing": pricing_inr}
            logging.info('dict is created')
        except:
            curriculum.append('NULL')
        return all_dict
    except:
        logging.error('Error in Scrapping at get_course()')


def scrap_all_mysql():
    try:
        final_list = []
        list_courses = all_course()
        for i in list_courses[0:5]:
            final_list.append(get_course_mysql(i))

        dataBase = mysql.connector.connect(host="localhost",passwd="",user="root",database="ineuron_scrapper")
        cursor = dataBase.cursor()

        for mydict in final_list:
            placeholders = ', '.join(['%s'] * len(mydict))
            columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in mydict.keys())
            values = ', '.join("'" +  str(x).replace('/', '_') + "'" for x in mydict.values())
            sql: str = "INSERT INTO tbl_courses ( %s ) VALUES ( %s );" % (columns, placeholders)
            cursor.execute(sql, list(mydict.values()))

        dataBase.commit()
        cursor.close()

    except Exception as e:
        logging.error("error in DB insertion", e)

def scrap_all_mongodb():
    dbcon = mongodbconnection(username='mongodbUser', password='Test@123')
    db_collection = dbcon.getCollection("mydb", "course_collection")
    try:
        if dbcon.isCollectionPresent("mydb", "course_collection"):
            pass
        else:
            final_list = []
            list_courses = all_course()
            for i in list_courses:
                final_list.append(get_course_mongo(i))
            db_collection.insert_many(final_list)
    except Exception as e:
        logging.error("error in DB insertion", e)

def get_course_mongo(coursename):
    ineuron_url = 'https://ineuron.ai/course/'
    uClient = uReq(ineuron_url + str(coursename).replace(" ", "-"))
    course_page = uClient.read()
    uClient.close()
    ineuron_html = bs(course_page, 'html.parser')
    course_data1 = json.loads(ineuron_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
    logging.info('Get courses by title')
    all_dict = {}
    # list = []
    try:
        try:
            all_data = course_data1["props"]["pageProps"]
        except:
            all_data = 'No page'
        try:
            page_data = all_data['data']
        except:
            page_data = 'No data'
        try:
            detailed_data = page_data['details']
        except:
            detailed_data = 'No details'
        try:
            meta_data = page_data['meta']
        except:
            meta_data = 'No meta_data'
        try:
            curriculum_data = meta_data['curriculum']
        except:
            curriculum_data = 'No curriculum_data'
        try:
            overview_data = meta_data['overview']
        except:
            overview_data = 'No overview_data'
        # Building a Course Dictionary
        try:
            pricing_inr = detailed_data['pricing']['IN']
        except:
            pricing_inr = 'NULL'
        try:
            course_name = page_data['title']
        except:
            course_name = 'Name NA'
        try:
            description = detailed_data['description']
        except:
            description = "NULL"
        try:
            language = overview_data['language']
        except:
            language = 'NULL'
        try:
            req = overview_data['requirements']
        except:
            req = 'NULL'
        try:
            learn = overview_data['learn']
        except:
            learn = 'NULL'
        curriculum = []
        try:
            for i in curriculum_data:
                curriculum.append(curriculum_data[i]["title"])
            all_dict = {"Course_title": course_name, "Description": description,
                        "Language": language, "Pricing": pricing_inr,
                        "Curriculum_data": curriculum, "Learn": learn,
                        "Requirements": req}
            logging.info('dict is created')
        except:
            curriculum.append('NULL')
        return all_dict
    except:
        logging.error('Error in Scrapping at get_course()')