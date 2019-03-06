from flask import Flask
from flask_login import LoginManager

from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app, prefix='/api/v1')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors

from app.api import bp as api_bp

app.register_blueprint(api_bp, url_prefix='/api')
