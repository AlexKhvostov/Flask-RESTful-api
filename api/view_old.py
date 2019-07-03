import logging
import json
from flask import Response

from app import db, api
from models import Worker, Department
from flask_restful import reqparse, abort, Resource
from flask_json import FlaskJSON, JsonError, json_response, as_json


''' show all Departments'''

parser = reqparse.RequestParser()
#Department
parser.add_argument('department')
#workers
parser.add_argument('department_id')
parser.add_argument('fullname')
parser.add_argument('birthday')
parser.add_argument('salary')
#filter by birthay
parser.add_argument('birthday_begin')
parser.add_argument('birthday_end')



class DepartmentList(Resource):
    def get(self):
        logging.info("*-*-*-*-*-* start GET (Department  LIST)*-*-*-*-*-*-*")
        department_list = {}
        department_all = Dept.query.all()
        for id in range(len(department_all)):
            department_list[department_all[id].id] = {'name': department_all[id].name}

        return department_list

    # add Department
    def post(self):
        logging.info("*-*-*-*-*-* start POST (Department  LIST)*-*-*-*-*-*-*")
        logging.info("start POST")
        args = parser.parse_args()

        logging.info("start POST , args : "+args['department'])
        print(args['department'])
        logging.info("end POST")

        department_add = Dept(name=args['department'])
        db.session.add(department_add)
        db.session.commit()
        return {'add Deportment: ': args['department']}


class WorkerList(Resource):
    # show all workers
    # will add filter by birthday
    #filter(and_(User.birthday >= '1988-01-17', User.birthday <= '1985-01-17'))
    def get(self):
        worker_list = {}
        args = parser.parse_args()

        logging.info("*-*-*-*-*-* start GET (workers_ LIST)*-*-*-*-*-*-*")


        if args['birthday_begin'] and args['birthday_end']:
            logging.info("*-*-*-*-*-*  use filter *-*-*-*-*-*-*")
            logging.info(" - 1 if")
            logging.info("birthday_begin : " + args['birthday_begin'])
            logging.info("birthday_end : " + args['birthday_end'])

            # worker_all = Workers.query.filter((Workers.birthday >= args['birthday_begin'], Workers.birthday <= args['birthday_end'])).all()
            worker_all = Workers.query.filter((Workers.birthday.between(args['birthday_begin'], args['birthday_end']))).all()
        elif args['birthday_begin']:
            logging.info("*-*-*-*-*-*  use filter *-*-*-*-*-*-*")
            logging.info(" - 1 elif")
            logging.info("birthday_begin : " + args['birthday_begin'])
            worker_all = Workers.query.filter(Workers.birthday >= args['birthday_begin']).all()
        elif args['birthday_end']:
            logging.info("*-*-*-*-*-*  use filter *-*-*-*-*-*-*")
            logging.info(" - 2 elif")
            logging.info("birthday_end : " + args['birthday_end'])
            worker_all = Workers.query.filter(Workers.birthday <= args['birthday_end']).all()
        else:
            worker_all = Workers.query.all()

        for id in range(len(worker_all)):
            worker_list[str(worker_all[id].id)] = {
                'name': worker_all[id].fullname,
                'department': Department.get(self, worker_all[id].deptname)['name'],
                'birthday': str(worker_all[id].birthday),
                'salary': worker_all[id].salary}

        return worker_list

    # add worker /
    # curl http://127.0.0.1:5000/worker -d "fullname=Anton Gorodetskij" -d "birthday=1991-02-02" -d "department_id=2" -d "salary=600" -X POST -v
    def post(self):
        logging.info("*-*-*-*-*-* start POST (workers_ LIST)*-*-*-*-*-*-*")
        args = parser.parse_args()
        logging.info("start POST , args : " + args['fullname']+" / " + args['department_id']+" / " + args['salary']+" / ")
        logging.info("start POST , args : " + args['fullname'])
        print(args['fullname'])
        logging.info("end POST")

        worker_add = Workers(deptname=args['department_id'], fullname=args['fullname'], birthday=args['birthday'], salary=args['salary'])
        db.session.add(worker_add)
        db.session.commit()
        return {'add worker': {
            'deptname': Department.get(self, args['department_id'])['name'],
            'fullname': args['fullname'],
            'birthday': args['birthday'],
            'salary': args['salary']
                }
            }


'''show (1)! one of all Deportments '''

class Department(Resource):
    def get(self, department_id=None):
        logging.info("*-*-*-*-*-* start GET (Department  LIST)*-*-*-*-*-*-*")

        if department_id:
            department_one = Dept.query.filter_by(id=department_id).first()
            department_list = {'id': department_id, 'name': "- not found"}
            if department_one:
                logging.info("*-*-*-*-*-*  "+str(department_one)+"  *-*-*-*-*-*-*")
                logging.info("*-*-*-*-*-  department_id- good  -*-*-*-*-*-*")
                department_list = {'id': department_id, 'name': department_one.name}

        else:
            logging.info("*-*-*-*-*-  department_id- not found  -*-*-*-*-*-*")
            department_list = {'id': department_id,
                               'name': "department_id- not found"}

        return department_list

    def delete(self, department_id = None):
        if department_id:
            logging.info("start DELETE DEPT , id : " + department_id)
            Dept.query.filter_by(id=department_id).delete()
            db.session.commit()
            logging.info("save to db : " + department_id)
            department_list = {' info. delete department :':  department_id}
        else:
            department_list = {' info :': ' department_id'}

        return department_list

    def put(self, department_id=None):
        #  curl http://127.0.0.1:5000/department/13 -d "department=teacher" -X PUT -v
        if department_id:
            logging.info("start PUT")
            args = parser.parse_args()
            deportment_one = Dept.query.filter_by(id=department_id).first()
            logging.info("start put / id "+department_id+", args : " + args['department'])
            deportment_one.name = args['department']
            logging.info("end PUT / deportment_one : " + deportment_one.name)

            try:
                db.session.commit()
            except Exception as ex:
                return Response(f'interval {ex!r}', status=500)
            department_list = {' edit id :': department_id}

        else:
            department_list = {' info :': ' department_id'}

        return Response(json.dumps(department_list), status=200)


'''show one of all Worker '''

class Worker (Resource):
    def get(self, worker_id = None):
        logging.info("*-*-*-*-*-* start GET (Worker  LIST)*-*-*-*-*-*-*")
        worker_one = Workers.query.filter_by(id=worker_id).first()
        if id:
            worker_list = {'id': worker_id,
                          'name': worker_one.fullname,
                          'department': Department.get(self, worker_one.deptname)['name'],
                          'birthday': str(worker_one.birthday),
                          'salary': worker_one.salary}
        else:
            worker_list = {' info :': ' error - invalid  worker_id or no worker_id'}

        return worker_list

    def delete(self, worker_id = None):
        if id:
            logging.info("start DELETE WORKER , id : " + worker_id)
            Workers.query.filter_by(id=worker_id).delete()
            db.session.commit()
            logging.info("save to db : " + worker_id)
            worker_list = {' info. delete worker :':  worker_id}

        else:
            worker_list = {}

        return worker_list

    def put(self, worker_id=None):
        if id:
            logging.info("*-*-*-*-*-* start PUT (workers)*-*-*-*-*-*-*")
            args = parser.parse_args()
            worker_one = Workers.query.filter_by(id=worker_id).first()
           # logging.info("start put / id " + worker_id + ", args : " + args['department_id']+", "+ args['fullname']+", "+ args['birthday']+", "+ args['salary']+".")
            if args['department_id']:
                worker_one.deptname = args['department_id']
            if args['fullname']:
                worker_one.fullname = args['fullname']
            if args['birthday']:
                worker_one.birthday = args['birthday']
            if args['salary']:
                worker_one.salary = args['salary']

            logging.info("end PUT / worker_one : " + worker_one.fullname)

            db.session.commit()
            worker_list = {' edit id :': worker_id}

            logging.info("*-*-*-*-*-* end PUT (workers)*-*-*-*-*-*-*")
        else:
            worker_list = {}

        return worker_list



# show list and add new item
api.add_resource(DepartmentList, '/department')
api.add_resource(WorkerList, '/worker')

# show, edit and delete one item by id
api.add_resource(Department, '/department/<department_id>')
api.add_resource(Worker, '/worker/<worker_id>')