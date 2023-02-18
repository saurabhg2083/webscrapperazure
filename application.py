import logging
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from mongodb import mongodbconnection
from getScrapDetails import all_course, get_course_mongo, scrap_all_mongodb, scrap_all_mysql
import configparser
import pymongo

logging.basicConfig(filename="sg_logs.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
application = Flask(__name__)
app = application
CORS(app)

dbname = "mydb"
collectionname = "course_collection"
dbcon = mongodbconnection(username='mongodbUser', password='Test@123')
course_coll = dbcon.getCollection(dbName='mydb', collectionName="course_collection")

# Connect to Flask
@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    # course_in = all_course()
    course_in = list(course_coll.find({}))
    logging.info("List of Course names Generated")
    return render_template("index.html", course_in=course_in)

@app.route('/course', methods=['POST', 'GET'])
@cross_origin()
def result():
    if request.method == 'POST':
        input_course = request.form['content'].replace("  ", " ")
        course_data = course_coll.find_one(
            {"Course_title": input_course}, {"_id": 0})
        logging.info("User input is taken and results Generated")
        return render_template("results.html", course_data=course_data)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
