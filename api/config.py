class Configuration(object):
    DEBUG = True
    # НАстройки доступа к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://alex:Protokol911#@localhost/flask'