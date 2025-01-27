from App import app, mail
from App.models.candidacies import Candidacy
from App.models.users import User
from flask_apscheduler import APScheduler
from flask import render_template
from flask_mail import Message
from datetime import datetime, timedelta
import os


def weekly_mail_to_users():
    today = datetime.utcnow().date()
    last_week = today - timedelta(days=7)
    with scheduler.app.app_context():
        candidacies = Candidacy.query.filter(
            Candidacy.date >= last_week, Candidacy.date < today
        ).all()

        user_candidacies = dict()
        for candidacy in candidacies:
            if user_candidacies.get(candidacy.user_id) is None:
                user_candidacies[candidacy.user_id] = list()
            user_candidacies[candidacy.user_id].append(candidacy)

        for user_id, candidacies in user_candidacies.items():
            # send a mail to every user with the candidacies that he need to contact once again
            user = User.query.get(user_id)

            msg = Message(
                "Tu devrais relancer ces entreprises.",
                sender=os.getenv("MAILER_ADRESSE"),
                recipients=[user.email],
            )  # mail could be an environnement variable

            msg.html = render_template(
                "/mail/weekly_renewal.html", user=user, candidacies=candidacies
            )

            try:
                mail.send(msg)
            except:
                continue


scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
