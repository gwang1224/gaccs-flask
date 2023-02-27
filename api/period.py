import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.periods import Period
from __init__ import db

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
            if periodlength is None:
                return {'message': f'Period length is missing'}, 400
            # validate score, score must be greater than 1
            cyclelength = body.get('cyclelength')
            if cyclelength is None:
                return {'message': f'Cycle length is missing'}, 400
            nextperiod = body.get('nextperiod')
            
            ''' #1: Key code block, setup USER OBJECT '''
            uo = Period(periodlength=periodlength,
                      cyclelength=cyclelength,
                      nextperiod=nextperiod)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Either a format error or period {nextperiod} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            periods = Period.query.all()    # read/extract all users from database
            json_ready = [period.read() for period in periods]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Delete(Resource):
        def delete(self):
            db.session.query(Period).delete()
            db.session.commit()
            return {'message': 'All records have been deleted.'}

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')
    