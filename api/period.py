import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.periods import Period

period_api = Blueprint('period_api', __name__,
                   url_prefix='/api/periods')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(period_api)

class PeriodAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            periodlength = body.get('periodlength')
            cyclelength = body.get('cyclelength')
            nextperiod = body.get('nextperiod')
            nextovulation = body.get('nextovulation')
            ''' #1: Key code block, setup USER OBJECT '''
            uo = Period(periodlength=periodlength,
                      cyclelength=cyclelength,
                      nextperiod=nextperiod,
                      nextovulation=nextovulation)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            periods = Period.query.all()    # read/extract all users from database
            json_ready = [period.read() for period in periods]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
                
    class _Readov(Resource):
        def get(self):
            periods = Period.query.all() 
            json_ready = [period.read() for period in periods] 
            data = []
            data.append(json_ready)
            # for i in data: 
            ovulation=[]
            for d in data:
                for dict in d:
                    ovulation.append( dict.get("nextovulation") )
            return ovulation
    
    class _Readovmonth(Resource):
        def get(self):
            periods = Period.query.all()    # read/extract all users from database
            json_ready = [period.read() for period in periods]  # prepare output in json
            data = []
            data.append(json_ready)
            print(data)
            # for i in data: 
            ovulationmonth=[]
            for d in data:
                for dict in d: 
                    ovulationmonth.append( dict.get("nextovulation").split()[0] )
            return ovulationmonth

    class _Readovday(Resource):
        def get(self):
            periods = Period.query.all()    # read/extract all users from database
            json_ready = [period.read() for period in periods]  # prepare output in json
            data = []
            data.append(json_ready)
            # for i in data: 
            ovulationday=[]
            for d in data:
                for dict in d:
                    ovulationday.append( dict.get("nextovulation").split()[1])
            return ovulationday
                    

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Readov, '/ov')
    api.add_resource(_Readovmonth, '/mo')
    api.add_resource(_Readovday, '/day')
    