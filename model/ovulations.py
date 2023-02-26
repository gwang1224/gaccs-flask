from random import randrange
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Ovulation(db.Model):
    __tablename__ = 'ovulations'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _nextovulation = db.Column(db.String(255), unique=True, nullable=False)
    _perioddate = db.Column(db.String(255), unique=True, nullable=False)
    _periodcycle = db.Column(db.String(255), unique=True, nullable=False)
    _menscycle = db.Column(db.String(255), unique=True, nullable=False)


    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # posts = db.relationship("Post", cascade='all, delete', backref='scores', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, nextovulation, perioddate, periodcycle, menscycle):
        self._nextovulation = nextovulation
        self._perioddate = perioddate
        self._periodcycle = periodcycle
        self._menscycle = menscycle

    @property
    def nextovulation(self):
        return self._nextovulation
    
    # a setter function, allows name to be updated after initial object creation
    @nextovulation.setter
    def nextovulation(self, nextovulation):
        self._nextovulation = nextovulation

    @property
    def perioddate(self):
        return self._perioddate
    # a setter function, allows name to be updated after initial object creation
    @perioddate.setter
    def perioddate(self, perioddate):
        self._perioddate = perioddate
    
    @property
    def periodcycle(self):
        return self._periodcycle
    # a setter function, allows name to be updated after initial object creation
    @periodcycle.setter
    def periodcycle(self, periodcycle):
        self._periodcycle = periodcycle

    @property
    def menscycle(self):
        return self._menscycle
    # a setter function, allows name to be updated after initial object creation
    @menscycle.setter
    def menscycle(self, menscycle):
        self._menscycle = menscycle
    
    @property
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "nextovulation": self.nextovulation,
            "perioddate": self.perioddate,
            "periodcycle": self.periodcycle,
            "menscycle": self.menscycle
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, nextovulation="", perioddate="", periodcycle="", menscycle=""):
        """only updates values with length"""
        if len(nextovulation) > 0:
            self.nextovulation = nextovulation
        if len(perioddate) > 0:
            self.perioddate = perioddate
        if len(periodcycle) > 0:
            self.periodcycle = periodcycle
        if len(menscycle) > 0:
            self.menscycle = menscycle
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initOvulations():
    with app.app_context():
        """Create database and tables"""
        #db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = Ovulation(nextovulation='January 25', perioddate='2023-01-15', periodcycle='5', menscycle='30')
        u2 = Ovulation(nextovulation='March 1', perioddate='2022-12-26', periodcycle='4', menscycle='28')
        u3 = Ovulation(nextovulation='August 13', perioddate='2023-03-15', periodcycle='7', menscycle='29')

        users = [u1, u2, u3]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.nextovulation + " note " + str(num) + ". \n Generated by test data."
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate ovulation, or error: {user.perioddate}")
            