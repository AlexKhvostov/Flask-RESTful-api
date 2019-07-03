import logging
import json
from flask import Response

from app import db, api
from models import Worker, Department
from flask_restful import reqparse, abort, Resource
from flask_json import FlaskJSON, JsonError, json_response, as_json


parser = reqparse.RequestParser()
parser.add_argument('department')


class DepartmentList(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class WorkerList(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(DepartmentList, '/department')
api.add_resource(WorkerList, '/worker')
