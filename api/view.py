import logging
import json
from flask import Response

from app import db, api
from models import Worker, Department
from flask_restful import reqparse, abort, Resource
from flask_json import FlaskJSON, JsonError, json_response, as_json


parser = reqparse.RequestParser()
parser.add_argument('department_name')
parser.add_argument('department_key')
parser.add_argument('worker_name')
parser.add_argument('birthday')
parser.add_argument("salary")


class DepartmentList(Resource):
    def get(self):
        pass

    def post(self):
        args = parser.parse_args()
        department_add = Department(department_name=args['department_name'])
        db.session.add(department_add)
        try:
            db.session.commit()
        except Exception as ex:
            return Response(f'interval {ex!r}', status=500)

        department_list = {'add_id': department_add.id,
                           'department_name': department_add.department_name}

        return Response(json.dumps(department_list), status=200)

    def put(self):
        pass

    def delete(self):
        pass


class WorkerList(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def post(self):
        args = parser.parse_args()
        worker_add = Worker(department_key=args['department_key'],
                            worker_name=args['worker_name'],
                            birthday=args['birthday'],
                            salary=args['salary'])
        db.session.add(worker_add)
        try:
            db.session.commit()
        except Exception as ex:
            return Response(f'interval {ex!r}', status=500)

        workers_list = {'add_id': worker_add.id,
                        'department_key': worker_add.department_key,
                        'worker_name': worker_add.worker_name,
                        'birthday': str(worker_add.birthday),
                        'salary': worker_add.salary}

        return Response(json.dumps(workers_list), status=200)

    def delete(self):
        args = parser.parse_args()
        Worker.query.filter_by(id=args['worker_id']).delete()
        db.session.commit()
        worker_list = {' info. delete worker :': args['worker_id']}
        return Response(json.dumps(worker_list), status=200)


api.add_resource(DepartmentList, '/department')
api.add_resource(WorkerList, '/worker')
