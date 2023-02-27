import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.ovulations import Ovulation
from __init__ import db

ovulation_api = Blueprint('ovulation_api', __name__,
                   url_prefix='/api/ovulation')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(ovulation_api)

class OvulationAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            perioddate = body.get('perioddate')
            periodcycle = body.get('periodcycle')
            menscycle = body.get('menscycle')
            ''' #1: Key code block, setup USER OBJECT '''
            uo = Ovulation(
                            perioddate=perioddate,
                            periodcycle=periodcycle,
                            menscycle=menscycle)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            #return {'message': f'Processed {perioddate}, either a format error or User ID {periodcycle} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            ovulations = Ovulation.query.all()    # read/extract all users from database
            json_ready = [ovulation.read() for ovulation in ovulations]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Delete(Resource):
        def delete(self):
            db.session.query(Ovulation).delete()
            db.session.commit()
            return {'message': 'All scores have been deleted.'}
                

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')
    