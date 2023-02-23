import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

# from model.symptoms import Symptom
from model.symptoms import Symptom

#database
symptom_api = Blueprint('symptom_api', __name__,
                   url_prefix='/api/symptom')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(symptom_api)

class SymptomAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # comment has to be longer than 5 characters
            comment = body.get('comment')
            if comment is None or len(comment) < 5:
                return {'message': f'Comment is missing, or is less than 5 characters'}, 400
            # comment has to be longer than 5 characters
            symptom = body.get('symptom')
            if symptom is None or len(symptom) < 2:
                return {'message': f'Symptom is missing, or is less than 5 characters'}, 400

            ''' #1: setup SYMPTOM OBJECT '''
            so = Symptom(comment=comment, 
                      symptom=symptom)
            
            
            ''' #2: Key Code block to add symptom to database '''
            # create user in database
            symptom = so.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {comment}, has a format error or {symptom} has a format error.'}, 400

    class _Read(Resource):
        def get(self):
            users = Symptom.query.all()    # read/extract all users from database
            json_ready = [symptom.read() for symptom in symptoms]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    