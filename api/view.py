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
parser.add_argument('birthday_finish')
parser.add_argument("salary")


class DepartmentList(Resource):
    def get(self):
        logging.debug("Start Class DepartmentList / method get")
        department_list = get_all_department()
        return Response(json.dumps(department_list), status=200)

    def post(self):
        logging.debug("Start Class DepartmentList / method post")
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
        logging.debug("Start Class WorkerList / method get")
        worker_list = get_all_worker()
        return Response(json.dumps(worker_list), status=200)

    def post(self):
        logging.debug("Start Class WorkerList / method post")
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

        # workers_list = {'add_id': worker_add.id,
        #                 'department_key': worker_add.department_key,
        #                 'worker_name': worker_add.worker_name,
        #                 'birthday': str(worker_add.birthday),
        #                 'salary': worker_add.salary}

        workers_list = get_all_department()
        return Response(json.dumps(workers_list), status=200)


class Department_one(Resource):
    def get(self, department_id=None):
        logging.debug("Start Class Department_one / method get / department_id : " + department_id)
        department_one = get_one_department(department_id)
        return Response(json.dumps(department_one), status=200)

    def put(self, department_id=None):
        logging.debug("Start Class Department_one / method put / department_id : " + department_id)
        args = parser.parse_args()
        #department_edit = get_one_department(department_id)
        if Department.query.filter_by(id=department_id).first():
            department_edit = Department.query.filter_by(id=department_id).first()
            if args['department_name']:
                department_edit.department_name = args['department_name']

            try:
                db.session.commit()
            except Exception as ex:
                return Response(f'interval {ex!r}', status=500)

            department_edit = get_one_department(department_id)

        return Response(json.dumps(department_edit), status=200)

    def delete(self, department_id=None):
        logging.debug("Start Class Department_one / method delete / department_id : " + department_id)
        Department.query.filter_by(id=department_id).delete()
        try:
            db.session.commit()
        except Exception as ex:
            return Response(f'interval {ex!r}', status=500)
        department_one = {' info. delete department :': department_id}
        return Response(json.dumps(department_one), status=200)


class Worker_one(Resource):
    def get(self, worker_id=None):
        logging.debug("Start Class Worker_one / method get / worker_id : " + worker_id)
        worker_list = get_one_worker(worker_id)
        return Response(json.dumps(worker_list), status=200)

    def put(self, worker_id=None):
        args = parser.parse_args()
        logging.debug("Start Class Worker_one / method put / worker_id : " + worker_id)
        worker_edit = get_one_worker(worker_id)
        if Worker.query.filter_by(id=worker_id).first():
            worker_edit = Worker.query.filter_by(id=worker_id).first()
            if args['department_key']:
                worker_edit.department_key = args['department_key']
                logging.debug("args['department_key'] : " + args['department_key'])
            if args['worker_name']:
                worker_edit.worker_name = args['worker_name']
                logging.debug("args['worker_name'] : " + args['worker_name'])
            if args['birthday']:
                worker_edit.birthday = args['birthday']
                logging.debug("args['birthday'] : " + args['birthday'])
            if args['salary']:
                worker_edit.salary = args['salary']
                logging.debug("args['salary'] : " + args['salary'])

            try:
                db.session.commit()
            except Exception as ex:
                return Response(f'interval {ex!r}', status=500)

            worker_edit = get_one_worker(worker_id)

        return Response(json.dumps(worker_edit), status=200)

    def delete(self, worker_id=None):
        logging.debug("Start Class Worker_one / method delete / worker_id : " + worker_id)
        Worker.query.filter_by(id=worker_id).delete()

        try:
            db.session.commit()
        except Exception as ex:
            return Response(f'interval {ex!r}', status=500)

        worker_del = {' info. delete worker :': worker_id}
        return Response(json.dumps(worker_del), status=200)


api.add_resource(DepartmentList, '/department')
api.add_resource(WorkerList, '/worker')
api.add_resource(Department_one, '/department/<department_id>')
api.add_resource(Worker_one, '/worker/<worker_id>')


def get_one_worker(worker_id):
    logging.debug("Start method get_one_worker / worker_id : " + worker_id)
    worker_list = {}
    worker_list[worker_id] = {
        'department_name': 'not found',
        'worker_name': 'not found',
        'birthday': 'not found',
        'salary': 'not found'
    }
    if Worker.query.filter_by(id=worker_id).first():
        worker_one = Worker.query.filter_by(id=worker_id).first()
        worker_list[worker_id] = {
            'department_name': get_name_department(worker_one.department_key),
            'worker_name': worker_one.worker_name,
            'birthday': str(worker_one.birthday),
            'salary': worker_one.salary
        }
    return worker_list


def filter_workers():
    logging.debug("Start method filter_workers ")
    args = parser.parse_args()
    if args['birthday_start'] and args['birthday_finish']:
        worker_filter = Worker.query.filter((Worker.birthday.between(args['birthday_start'], args['birthday_finish']))).all()
    elif args['birthday_start']:
        worker_filter = Worker.query.filter(Worker.birthday >= args['birthday_start']).all()
    elif args['birthday_finish']:
        worker_filter = Worker.query.filter(Worker.birthday <= args['birthday_finish']).all()
    else:
        worker_filter = Worker.query.all()

    return worker_filter


def get_all_worker():
    logging.debug("Start method get_all_worker ")
    worker_list = {}
    worker_all = filter_workers()
    for id in range(len(worker_all)):
        worker_list[str(worker_all[id].id)] = {
            'department_name': get_name_department(worker_all[id].department_key),
            'worker_name': worker_all[id].worker_name,
            'birthday': str(worker_all[id].birthday),
            'salary': worker_all[id].salary
        }
    return worker_list


def get_one_department(department_id):
    logging.debug("Start method get_one_department / department_id : " + str(department_id))
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
    logging.debug("Start method get_all_department ")
    department_list = {}
    department_one = Department.query.all()
    for id in range(len(department_one)):
        department_list[str(department_one[id].id)] = {
            'department_name': department_one[id].department_name,
            'average_salary': average_salary(department_one[id].id)
        }
    return department_list


def get_name_department(department_id):
    logging.debug("Start method get_name_department ")
    department = get_one_department(department_id)
    name = department[department_id]['department_name']
    return name


def average_salary(department_id):
    logging.debug("Start method average_salary ")
    worker = Worker.query.all()

    delta = 0
    k = 0

    for i in worker:
        if i.department_key == int(department_id):
            delta += int(i.salary)
            k += 1

    try:
        delta = delta / k
    except ZeroDivisionError:
        delta = 0

    return delta



