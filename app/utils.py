import os
import configparser
from enum import Enum

CONFIG_FILE_PATH = os.path.join(os.getcwd(), 'aircompany.ini')


class Context:
    """
    Cotains parser methods of config from a different number of sections of CONFIG_FILE_PATH
    """
    @classmethod
    def get(cls, parameter):
        """
        Takes params from [db] section of ini file
        :param parameter:
        :return: value from a parameter as str
        """
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        return config.get('config', parameter.value)


class Parameter(Enum):
    DB_USERNAME = 'dbuser'
    DB_PASSWORD = 'dbpassword'
    DB_HOST = 'dbhost'
    DB_NAME = 'dbname'
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'sqlalchemy_track_modifications'
    USER_EMAIL_SENDER_EMAIL = 'user_mail_sender_email'
