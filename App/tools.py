from functools import wraps
from flask import redirect, url_for, flash
from App import app, app, mail
from flask_login import current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from random import *
import os


def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.is_admin != 1:
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("home_page"))
        return func(*args, **kwargs)

    return decorator


def send_mail(title, body, email):
    msg = Message(
        f"{title}", sender=os.getenv("MAILER_ADRESSE"), recipients=[f"{email}"]
    )
    msg.body = f"{body}"
    mail.send(msg)


def generate_confirmation_token(data):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(data, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        data = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except:
        return False
    return data
