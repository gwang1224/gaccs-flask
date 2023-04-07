import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
# from model.users import User
from model.symptoms import Symptom

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
            # validate name
            comment = body.get('comment')
            if comment is None or len(comment) < 2:
                return {'message': f'Comment is missing, or is less than 2 characters'}, 400
            # validate symptom
            symptom = body.get('symptom')
            if symptom is None or len(symptom) < 2:
                return {'message': f'Symptom is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Symptom(comment=comment, 
                      symptom=symptom)
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {comment}, either a format error or {symptom} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            users = Symptom.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            sid = body.get('sid')
            sym = Symptom.query.get(sid)
            sym.delete()
            #return f"{score.read()} Has been deleted"

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Delete, '/delete')
    api.add_resource(_Read, '/')