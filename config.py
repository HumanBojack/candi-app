import os

# Database initialization
if os.environ.get("DATABASE_URL"):
    path = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = path.replace("postgres://", "postgresql://", 1)
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

SECRET_KEY = "VerySecret"
SECURITY_PASSWORD_SALT = "MyVerySecretTwo"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Jobs configuration
JOBS = [
    {
        "id": "mailer",
        "func": "App.jobs:weekly_mail_to_users",
        "trigger": "cron",
        "day_of_week": "mon",
        "hour": 18,
    }
]
SCHEDULER_API_ENABLED = True
SCHEDULER_TIMEZONE = "Europe/Paris"

# Mail configuration
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USERNAME = os.getenv("MAILER_ADRESSE")
MAIL_PASSWORD = os.getenv("MAILER_PASSSWORD")
MAIL_USE_TLS = False
MAIL_USE_SSL = True
