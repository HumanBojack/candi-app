from App import app, mail
from .models import User, Candidacy
from flask_apscheduler import APScheduler
from flask import render_template
from flask_mail import Message
from datetime import datetime, timedelta


def weekly_mail_to_users():
    today = datetime.utcnow().date()
    last_week = today - timedelta(days=7)
    with scheduler.app.app_context():
        candidacies = Candidacy.query.filter(
            Candidacy.date >= last_week, Candidacy.date < today
        ).all()

        user_candidacies = dict()
        for candidacy in candidacies:
            # user = user_candidacies.get(candidacy.user_id, None)
            # if user is None:
            #     user_candidacies[candidacy.user_id] = list()
            if user_candidacies.get(candidacy.user_id) is None:
                user_candidacies[candidacy.user_id] = list()
            user_candidacies[candidacy.user_id].append(candidacy)
        print(user_candidacies)

        for user_id, candidacies in user_candidacies.items():
            # send a mail to every user with the candidacies that he need to contact once again
            # print(User.query.get(user_id).email)
            print(candidacies[0].company.name)
            user = User.query.get(user_id)

            msg = Message(
                "Tu devrais relancer ces entreprises.",
                sender="candi.app.mailer@gmail.com",
                recipients=[user.email],
            )  # mail could be an environnement variable

            msg.html = render_template(
                "/mail/weekly_renewal.html", user=user, candidacies=candidacies
            )

            try:
                mail.send(msg)
            except:
                continue

        # print(candidacy.contact_full_name)
        print("done")


scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
