from app import db


# описание объектов в базе данных
class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_key = db.Column(db.Integer)
    name = db.Column(db.String(30))
    birthday = db.Column(db.Date)
    salary = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '(id: {}, worker_name: {}, department_key: {}, birthday: {}, salary: {})'\
            .format(self.id, self.fullname, self.deptname, self.birthday, self.salary)


# описание объектов в базе данных
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(30))

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '(id: {}, department: {})'.format(self.id, self.name)
