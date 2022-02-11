from this import d
from App import app
from .models import User, Candidacy
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta

def weekly_mail_to_users():
  today = datetime.utcnow().date()
  last_week = today - timedelta(days=7)
  with scheduler.app.app_context():
    # candidacies = Candidacy.query.filter(Candidacy.date >= last_week, Candidacy.date < today).all()
    # candidacies = Candidacy.query.filter(datetime.strptime(Candidacy.date, "%Y-%m-%d") >= last_week & datetime.strptime(Candidacy.date, "%Y-%m-%d") < today)
    # candidacies = Candidacy.query.filter(Candidacy.date >= last_week).all()
    # print(candidacies)
    # for candidacy in candidacies:
    #   print("one candidacy")
    print("done")

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()