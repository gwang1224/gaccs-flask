import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

# from model.users import User
from model.comments import Comment1

comment1_api = Blueprint('comment1_api', __name__,
                   url_prefix='/api/comment1')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(comment1_api)

class Comment1API:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate comment
            comment1 = body.get('comment1')
            if comment1 is None or len(comment1) < 2:
                return {'message': f'Your comment is missing, or is less than 2 characters'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Comment1(comment1=comment1)
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {comment1}, either a format error or User ID is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            users = Comment1.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    

            

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    