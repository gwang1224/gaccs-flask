from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.symptoms import Symptom

symptom_bp = Blueprint("symptom", __name__)
symptom_api = Api(symptom_bp)


class SymptomAPI(Resource):
    def get(self):
        id = request.args.get("id")
        symptom = db.session.query(Symptom).get(id)
        if symptom:
            return symptom.to_dict()
        return {"message": "symptom not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("comment", required=True, type=str)
        parser.add_argument("symptom", required=False, type=int)
        
        args = parser.parse_args()

        symptom = Symptom(args["comment"], args["symptoms"])
        try:
            db.session.add(symptom)
            db.session.commit()
            return symptom.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            symptom = db.session.query(Symptom).get(args["id"])
            if symptom:
                symptom.started = False
                db.session.commit()
            else:
                return {"message": "symptom not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            symptom = db.session.query(Symptom).get(args["id"])
            if symptom:
                db.session.delete(symptom)
                db.session.commit()
                return symptom.to_dict()
            else:
                return {"message": "symptom not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


class SymptomListAPI(Resource):
    def get(self):
        symptoms = db.session.query(Symptom).all()
        return [symptom.to_dict() for symptom in symptoms]


symptom_api.add_resource(SymptomAPI, "/symptom")
symptom_api.add_resource(SymptomListAPI, "/symptomList")