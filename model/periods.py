""" database dependencies to support sqliteDB examples """
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
class Period(db.Model):
    __tablename__ = 'periods'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _comment = db.Column(db.String(255), unique=False, nullable=False)
    _symptom = db.Column(db.String(255), unique=True, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # posts = db.relationship("Post", cascade='all, delete', backref='scores', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, periodlength, cyclelength, nextperiod, nextovulation):
        self._periodlength = periodlength    # variables with self prefix become part of the object, 
        self._cyclelength = cyclelength
        self._nextperiod = nextperiod
        self._nextovulation = nextovulation

    # a name getter method, extracts name from object
    @property
    def periodlength(self):
        return self._periodlength
    
    # a setter function, allows name to be updated after initial object creation
    @periodlength.setter
    def comment(self, periodlength):
        self._periodlength = periodlength
    
    # a getter method, extracts email from object
    @property
    def cyclelength(self):
        return self._cyclelength
    
    # a setter function, allows name to be updated after initial object creation
    @cyclelength.setter
    def symptom(self, cyclelength):
        self._cyclelength = cyclelength

        # a getter method, extracts email from object
    @property
    def nextperiod(self):
        return self._nextperiod
    
    # a setter function, allows name to be updated after initial object creation
    @nextperiod.setter
    def nextperiod(self, nextperiod):
        self._nextperiod = nextperiod
    
    @property
    def nextovulation(self):
        return self._nextovulation
    
    # a setter function, allows name to be updated after initial object creation
    @nextovulation.setter
    def nextovulation(self, nextovulation):
        self._nextovulation = nextovulation
        
    # check if uid parameter matches user id in object, return boolean
    def is_nextperiod(self, nextperiod):
        return self._nextperiod == nextperiod
    
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
            "periodlength": self.periodlength,
            "cyclelength": self.cyclelength,
            "nextperiod": self.nextperiod,
            "nextovulation": self.nextovulation
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, periodlength="", cyclelength="", nextperiod="", nextovulation=""):
        """only updates values with length"""
        if len(periodlength) > 0:
            self.periodlength = periodlength
        if len(cyclelength) > 0:
            self.cyclelength = cyclelength
        if len(nextperiod) > 0:
            self.nextperiod = nextperiod
        if len(nextovulation) > 0:
            self.nextovulation = nextovulation
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
def initPeriods():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = Period(periodlength='5', cyclelength='30', nextperiod='February 23rd')
        u2 = Period(periodlength='4', cyclelength='25', nextperiod='February 28th')
        u3 = Period(periodlength='7', cyclelength='40', nextperiod='February 21st')
        u4 = Period(periodlength='4', cyclelength='21', nextperiod='February 19th ')

        users = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.nextperiod + " note " + str(num) + ". \n Generated by test data."
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate period, or error: {user.cyclelength}")
            