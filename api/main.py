import logging
import view

from app import app


logging.basicConfig(
    filename="Logging.log",
    filemode="w",
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG)


# код для запуска сервиса
if __name__ == '__main__':
    app.run()
