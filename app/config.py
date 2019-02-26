import os
from .utils import Context, Parameter

get = lambda x: Context.get(x)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(get(Parameter.DB_USERNAME),
                                                                   get(Parameter.DB_PASSWORD),
                                                                   get(Parameter.DB_HOST),
                                                                   get(Parameter.DB_NAME))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
