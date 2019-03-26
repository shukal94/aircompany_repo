from elasticsearch import Elasticsearch
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment

from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors

from app.api import bp as api_bp

app.register_blueprint(api_bp, url_prefix='/api/v1')
bootstrap = Bootstrap(app)
moment = Moment(app)
app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) if app.config['ELASTICSEARCH_URL'] else None
