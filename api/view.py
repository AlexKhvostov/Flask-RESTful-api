import logging
import json
from flask import Response

from app import db, api
from models import Worker, Department
from flask_restful import reqparse, abort, Resource
from flask_json import FlaskJSON, JsonError, json_response, as_json


parser = reqparse.RequestParser()
parser.add_argument("worker_id")
parser.add_argument("department_id")
parser.add_argument('department_name')
parser.add_argument('department_key')
parser.add_argument('worker_name')
parser.add_argument('birthday')
parser.add_argument('birthday_start')
parser.add_argument('birthday_end')
parser.add_argument("salary")




class DepartmentList(Resource):
    def get(self):
        department_list = get_all_department()
        return Response(json.dumps(department_list), status=200)

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


class WorkerList(Resource):
    def get(self):
        worker_list = get_all_worker()
        return Response(json.dumps(worker_list), status=200)

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


class Department_one(Resource):
    def get(self, department_id=None):

        department_one = get_one_department(department_id)
        return Response(json.dumps(department_one), status=200)

    def put(self, department_id=None):
        args = parser.parse_args()
        department_edit = get_one_department(department_id)
        if Department.query.filter_by(id=department_id).first():
            department_edit = Worker.query.filter_by(id=department_id).first()
            if args['department_name']:
                department_edit.department_name = args['department_name']

            try:
                db.session.commit()
            except Exception as ex:
                return Response(f'interval {ex!r}', status=500)

            department_edit = get_one_department(department_id)

        return Response(json.dumps(department_edit), status=200)

    def delete(self, department_id=None):
        Department.query.filter_by(id=department_id).delete()
        try:
            db.session.commit()
        except Exception as ex:
            return Response(f'interval {ex!r}', status=500)
        department_one = {' info. delete department :': department_id}
        return Response(json.dumps(department_one), status=200)


class Worker_one(Resource):
    def get(self, worker_id=None):
        worker_list = get_one_worker(worker_id)
        return Response(json.dumps(worker_list), status=200)

    def put(self, worker_id=None):
        args = parser.parse_args()
        worker_edit = get_one_worker(worker_id)
        if Worker.query.filter_by(id=worker_id).first():
            worker_edit = Worker.query.filter_by(id=worker_id).first()
            if args['department_key']:
                worker_edit.department_key = args['department_key']
            if args['worker_name']:
                worker_edit.worker_name = args['worker_name']
            if args['birthday']:
                worker_edit.birthday = args['birthday']
            if args['salary']:
                worker_edit.salary = args['salary']

            try:
                db.session.commit()
            except Exception as ex:
                return Response(f'interval {ex!r}', status=500)
            worker_edit = get_one_worker(worker_id)

        return Response(json.dumps(worker_edit), status=200)

    def delete(self, worker_id=None):
        Worker.query.filter_by(id=worker_id).delete()
        db.session.commit()
        worker_del = {' info. delete worker :': worker_id}
        return Response(json.dumps(worker_del), status=200)


api.add_resource(DepartmentList, '/department')
api.add_resource(WorkerList, '/worker')
api.add_resource(Department_one, '/department/<department_id>')
api.add_resource(Worker_one, '/worker/<worker_id>')



def get_one_worker(worker_id):
    worker_list = {}
    worker_list[worker_id] = {
        'department_key': 'not found',
        'worker_name': 'not found',
        'birthday': 'not found',
        'salary': 'not found'
    }
    if Worker.query.filter_by(id=worker_id).first():
        worker_one = Worker.query.filter_by(id=worker_id).first()
        worker_list[worker_id] = {
            'department_key': worker_one.department_key,
            'worker_name': worker_one.worker_name,
            'birthday': str(worker_one.birthday),
            'salary': worker_one.salary
        }
    return worker_list


def get_all_worker():
    worker_list = {}
    worker_all = Worker.query.all()
    for id in range(len(worker_all)):
        worker_list[str(worker_all[id].id)] = {
            'department_key': worker_all[id].department_key,
            'worker_name': worker_all[id].worker_name,
            'birthday': str(worker_all[id].birthday),
            'salary': worker_all[id].salary
        }
    return worker_list


def get_one_department(department_id):
    department_list = {}
    department_list[department_id] = {
        'department_name': "not found"
    }

    if Department.query.filter_by(id=department_id).first():
        department_one = Department.query.filter_by(id=department_id).first()
        department_list[department_id] = {
            'department_name': department_one.department_name
        }
    return department_list


def get_all_department():
    department_list = {}
    department_one = Department.query.all()
    for id in range(len(department_one)):
        department_list[str(department_one[id].id)] = {
            'department_name': department_one[id].department_name
        }
    return department_list
