import threading

# import "packages" from flask
from flask import render_template, Flask, jsonify, request  # import render_template from "public" flask libraries
import sqlite3
# import "packages" from "this" project
from __init__ import app, db # Definitions initialization
from model.jokes import initJokes
from model.users import initUsers
from model.scores import initScores
from model.symptoms import initSymptoms
from model.periods import initPeriods
from model.comments import initComments
from model.ovulations import initOvulations


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.score import score_api
from api.symptom import symptom_api
from api.period import period_api
from api.comment import comment1_api
from api.ovulation import ovulation_api

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(score_api)
app.register_blueprint(symptom_api)
app.register_blueprint(period_api)
app.register_blueprint(comment1_api)
app.register_blueprint(ovulation_api)

def db_connection():
    conn = None
    try: 
        conn = sqlite3.connect('periods.sqlite')
    except sqlite3.error as e: 
        print(e)
    return conn 

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

#@app.route('/nextovulation', methods = ["GET"])
#def nextov():
  #  if request.method == "GET":
   #     conn = db_connection()
   #     cursor = conn.cursor("SELECT * FROM sqlite.db")
   #     result = cursor.fetchall()
   #     if result is not None:
    #        return result.jsonify()
    #    else: 
    #        return "Something wrong", 404


@app.before_first_request
def activate_job():
    db.init_app(app)
    initJokes()
    initUsers()
    initPeriods()
    initComments()
    initScores()
    initSymptoms()
    initOvulations()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8087")