from App import app
from .models import User
from flask_apscheduler import APScheduler
# @app.cli.command()
# def weekly_mail_to_users():
#   print("Salut à tous !!!")
#   print(str(User.query.all()))

#    $ flask run
#* * * * * cd /Users/rom1/Documents/VSCode/candi-app/ && FLASK_APP=run.py /Users/rom1/opt/anaconda3/envs/flask/bin/python flask weekly-mail-to-users >>mail.log 2>&1
# * * * * * cd /Users/rom1/Documents/VSCode/candi-app/ && FLASK_APP=run.py /Users/rom1/opt/anaconda3/envs/flask/bin/flask weekly-mail-to-users >>mail.log 2>&1

print("working")

def mailer():
  print("Salut !")

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()