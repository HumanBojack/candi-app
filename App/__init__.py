from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api

from security import authenticate, identity

app = Flask(__name__)

app.config.from_object('config')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'candi.app.mailer@gmail.com'
app.config['MAIL_PASSWORD'] = 'Zqrav47?trak!76'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
api = Api(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from App import routes
from App import models

