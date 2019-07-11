import requests
import logging

from app import app
from flask import render_template, request


def get_parameters():
    logging.debug("start  get_parameters ")
    arguments = {
        'department_name': request.form.get('department_name'),
        'worker_name': request.form.get('worker_name'),
        'department_key': request.form.get('department_key'),
        'birthday': request.form.get('birthday'),
        'salary': request.form.get('salary'),
        'birthday_start': request.form.get('birthday_start'),
        'birthday_finish': request.form.get('birthday_finish'),
    }
    return arguments


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/workers', methods=['GET', 'POST'])
def workers():
    url = 'http://127.0.0.1:5000/worker'

    if request.form.get('add'):
        item_add(url)

    if request.form.get('edit'):
        item_edit(url)

    if request.form.get('delete'):
        item_del(url)

    department_all = get_departments()

    if request.form.get('filter_date'):
        worker_all = get_workers(get_parameters())

    else:
        worker_all = get_workers()
    filter_date = {
        'birthday_start': request.form.get('birthday_start'),
        'birthday_finish': request.form.get('birthday_finish')
    }

    return render_template('workers.html', worker=worker_all, date_filter=filter_date, department=department_all )


@app.route('/departments', methods=['GET', 'POST'])
def departments():
    url = 'http://127.0.0.1:5000/department'

    if request.form.get('add'):
        item_add(url)

    if request.form.get('edit'):
        item_edit(url)

    if request.form.get('delete'):
        item_del(url)

    department_all = get_departments()

    return render_template('departments.html', department=department_all)


def item_add(url):
    logging.debug("start  item_add " + url)
    args = get_parameters()
    resp = requests.post(url, args).json()

    #
    # if resp.status == 500:
    #     return "error / db not edit"
    # else:
    #     return resp
    return resp


def item_edit(url):
    logging.debug("start  item_edit " + url)
    args = get_parameters()
    if request.form.get('edit'):
        url = url + "/" + str(request.form.get('edit'))
    resp = requests.put(url, args).json()
    return resp


def item_del(url):
    logging.debug("start  item_del "+url)
    if request.form.get('delete'):
        url = url + "/" + str(request.form.get('delete'))
    resp = requests.delete(url).json()
    return resp


def get_workers(filter_date=""):
    return requests.get('http://127.0.0.1:5000/worker', filter_date).json()


def get_departments():
    return requests.get('http://127.0.0.1:5000/department').json()