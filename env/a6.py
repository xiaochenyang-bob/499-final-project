from flask import Flask, render_template, request
import requests
import json
import pymysql

class People:
    def __init__(self,firstname, lastname, birthday, country):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.country = country

app = Flask(__name__)
# people = []
# connect to database
db = pymysql.connect("localhost","root","11433020Abc","TESTDB" )
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS PEOPLE")
sql = """CREATE TABLE PEOPLE (
   FIRST_NAME  CHAR(20) NOT NULL,
   LAST_NAME  CHAR(20) NOT NULL,
   BIRTHDAY DATE,  
   COUNTRY CHAR(20)
   )"""
cursor.execute(sql);


@app.route("/")
def index():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    birthday = request.args.get("birthday")
    country = request.args.get("country")
    if firstname and lastname and birthday and country:
        sql = """INSERT INTO PEOPLE(FIRST_NAME,
           LAST_NAME, BIRTHDAY, COUNTRY)
           VALUES ('%s', '%s', '%s', '%s')""" % (firstname, lastname, birthday, country)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # person = People(firstname, lastname, birthday, country)
        # people.append(person)
    sql = "SELECT * FROM PEOPLE"
    cursor.execute(sql)
    results = cursor.fetchall()
    people = []
    for row in results:
        firstname = row[0]
        lastname = row[1]
        birthday = row[2]
        country = row[3]
        person = People(firstname, lastname, birthday, country)
        people.append(person)
    return render_template("index.html", people=people )

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/personView")
def detail():
    fullname = request.args.get("fullname")
    names = fullname.split('_')
    firstname = names[0]
    lastname = names[1]
    sql = "SELECT * FROM PEOPLE WHERE FIRST_NAME = '%s' AND LAST_NAME = '%s'" % (firstname, lastname)
    firstname=""
    lastname=""
    birthday=""
    country=""
    try:
        rows_count = cursor.execute(sql)
        if rows_count == 0:
            return render_template("errorPage.html")
        results = cursor.fetchone()
        firstname = results[0]
        lastname = results[1]
        birthday = results[2]
        country = results[3]
        print("fname = %s,lname = %s,birthday = %s,country = %s" % \
              (firstname, lastname, birthday, country))
    except:
        print("Error: unable to fetch data")
    selectPerson = People(firstname, lastname, birthday, country)
    countryInfo = requests.get('https://restcountries.eu/rest/v2/name/' + selectPerson.country)
    if countryInfo.status_code == 200:
        info = countryInfo.json()
        return render_template("personView.html", person=selectPerson, countryInfo=info[0])
    else:
        return render_template("personView.html", person=selectPerson, countryInfo=None)
    # for person in people:
    #     if firstname == person.firstname:
    #         selectPerson = person
    #         countryInfo = requests.get('https://restcountries.eu/rest/v2/name/' + selectPerson.country)
    #         if countryInfo.status_code == 200:
    #             info = countryInfo.json()
    #             return render_template("personView.html", person = selectPerson, countryInfo = info[0])
    #         else:
    #             return render_template("personView.html", person = selectPerson, countryInfo = None)
    #return render_template("index.html", people=people)

if __name__ == "__main__":
    app.run(debug=True)