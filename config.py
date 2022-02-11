import os

#Database initialization
if os.environ.get("DATABASE_URL"):
    path = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = path.replace("postgres://", "postgresql://", 1)
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SECRET_KEY = 'VerySecret'
SECURITY_PASSWORD_SALT = 'MyVerySecretTwo'
SQLALCHEMY_TRACK_MODIFICATIONS = False

JOBS = [
    {
        "id": "mailer",
        "func": "App.jobs:mailer",
        "trigger": "interval",
        "seconds": 10
    }
]
SCHEDULER_API_ENABLED = True


