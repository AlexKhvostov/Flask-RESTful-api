import requests
import logging

from app import app
from flask import render_template, request


@app.route('/', methods=['GET', 'POST'])
def index():
    # filter_date = {'birthday_begin': '1950-01-01', 'birthday_end': '2020-01-01'}
    filter_date = {}
    logging.info(" ### start index ### ")

    logging.info(" ##################################### ")
    logging.info(" ### start deferent if method =GET ### ")


    if request.form.get('worker_add'):
        logging.info("method POST.   fullname   :"+request.form.get('fullname'))
        post_arguments = {'fullname': request.form.get('fullname'),
                          'department_id': request.form.get('department_id'),
                          'birthday': request.form.get('birthday'),
                          'salary': request.form.get('salary')}
        requests.post('http://127.0.0.1:5000/worker', post_arguments)
    else:
        logging.info("NOT TRUE   -    fullname         =-=  method POST. ")

    if request.form.get('department_add'):
        logging.info(" method POST. department_add : " + request.form.get('department_add'))
        post_arguments = {'department': request.form.get('department_add')}
        requests.post('http://127.0.0.1:5000/department', post_arguments)
    else:
        logging.info("NOT TRUE   -  department_add     =-=  method POST. ")

    if request.form.get('worker_delete'):
        logging.info(" ### start if worker_delete ### ")
        logging.info("worker_delete =-=  method DELETE. " + request.form.get('worker_delete'))
        requests.delete('http://127.0.0.1:5000/worker/'+str(request.form.get('worker_delete')))
    else:
        logging.info("NOT TRUE   -  worker_delete     =-=  method DELETE. ")

    if request.form.get('department_delete'):
        logging.info(" ### start if department_delete ### ")
        logging.info("department_delete =-=  method DELETE. " + request.form.get('department_delete'))
        requests.delete('http://127.0.0.1:5000/department/' + str(request.form.get('department_delete')))
    else:
        logging.info("NOT TRUE   -  department_delete =-=  method DELETE. ")

    if request.form.get('birthday_begin'):
        filter_date['birthday_begin'] = str(request.form.get('birthday_begin'))
    else:
        logging.info("NOT TRUE   -   birthday_begin   =-=  method get. ")

    if request.form.get('birthday_end'):
        filter_date['birthday_end'] = str(request.form.get('birthday_end'))
    else:
        logging.info("NOT TRUE   -   birthday_end     =-=  method get. ")

    if request.form.get('department_edit'):
        logging.info(" ### start if department_edit ### ")
        department_edit = {'id': request.form.get('department_edit'),
                           'department': request.form.get('department_name')}
        resp = requests.put('http://127.0.0.1:5000/department/'+request.form.get('department_edit'), department_edit).json()
        #
        # if resp.status == 500:
        #     sadfsakdjfksajfdlk
        # else:
        #     ssdfsdfsaf
    else:
        logging.info("NOT TRUE   -   department_edit   =-=  method put. ")

    if request.form.get('worker_edit'):
        logging.info(" ### start if   worker_edit    ### ")
        department_edit = {'department_id': request.form.get('department'),
                           'fullname': request.form.get('fullname'),
                           'birthday': request.form.get('birthday'),
                           'salary': request.form.get('salary')}

        requests.put('http://127.0.0.1:5000/worker/'+request.form.get('worker_edit'), department_edit).json()

    else:
        logging.info("NOT TRUE   -   worker_edit   =-=  method put. ")

    logging.info(" ### end all if  ### ")

    departments = requests.get('http://127.0.0.1:5000/department').json()
    if filter_date:
        workers = requests.get('http://127.0.0.1:5000/worker', filter_date).json()
    else:
        workers = requests.get('http://127.0.0.1:5000/worker').json()

    logging.info(" ### end index ### ")

    for i in departments:
        salary_sum = 0
        num = 0
        for j in workers:
            if departments[i]['name'] == workers[j]['department']:
                salary_sum += int(workers[j]['salary'])
                num += 1

        if num:
            delta_salary = salary_sum / num
        else:
            delta_salary = 0
        departments[i]['delta_salary'] = delta_salary
    return render_template('departments.html', name=workers, depart=departments, date=filter_date)


def item_add():
    pass


def item_edit():
    pass


def item_del():
    pass


def item_show():
    pass
