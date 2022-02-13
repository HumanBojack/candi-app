from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api
from dotenv import load_dotenv


load_dotenv(override=True)

app = Flask(__name__)

app.config.from_object("config")

api = Api(app)

# api.add_resource()

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from App import jobs
from App import routes
from App import models
