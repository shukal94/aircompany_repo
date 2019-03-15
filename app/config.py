import os
from .utils import Context, Parameter

get = lambda x: Context.get(x)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or get(Parameter.SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        get(Parameter.DB_USERNAME),
        get(Parameter.DB_PASSWORD),
        get(Parameter.DB_HOST),
        get(Parameter.DB_NAME)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = eval(
        get(Parameter.SQLALCHEMY_TRACK_MODIFICATIONS)
    )
    USER_EMAIL_SENDER_EMAIL = get(Parameter.USER_EMAIL_SENDER_EMAIL)
