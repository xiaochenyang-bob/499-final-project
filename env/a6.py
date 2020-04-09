from flask import Flask, render_template, request
import requests
import json
class People:
    def __init__(self,firstname, lastname, birthday, country):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.country = country

app = Flask(__name__)
people = []

@app.route("/")
def index():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    birthday = request.args.get("birthday")
    country = request.args.get("country")
    if firstname and lastname and birthday and country:
        person = People(firstname, lastname, birthday, country)
        people.append(person)
    return render_template("index.html", people=people)

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/personView")
def detail():
    fullname = request.args.get("fullname")
    names = fullname.split('_')
    firstname = names[0]
    for person in people:
        if firstname == person.firstname:
            selectPerson = person
            countryInfo = requests.get('https://restcountries.eu/rest/v2/name/' + selectPerson.country)
            if countryInfo.status_code == 200:
                info = countryInfo.json()
                return render_template("personView.html", person = selectPerson, countryInfo = info[0])
            else:
                return render_template("personView.html", person = selectPerson, countryInfo = None)
    return render_template("index.html", people=people)

if __name__ == "__main__":
    app.run(debug=True)