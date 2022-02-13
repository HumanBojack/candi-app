import csv
from App import db
import logging as lg
from werkzeug.security import generate_password_hash
from App.models.companies import Company
from App.models.locations import Location
from App.models.users import User

def init_db():
    db.session.commit()
    db.drop_all()
    db.create_all()


def seed_db():
    User(
        email="cb@gmail.com",
        password=generate_password_hash("1234", method="sha256"),
        last_name="ben",
        first_name="charles",
        is_admin=1,
    ).save_to_db()
    User(
        email="bb@gmail.com",
        password=generate_password_hash("1234", method="sha256"),
        last_name="beniac",
        first_name="cha",
        is_admin=0,
        promotion="Dev IA",
    ).save_to_db()

    # Import and creates regions
    with open("App/static/seed/regions.csv", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        regions_data = list(reader)
    for region in regions_data:
        location = {"region": region[0]}
        Location(**location).save_to_db()

    # Import and create companies
    with open("App/static/seed/companies.csv", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        companies_data = list(reader)
    for i in companies_data:
        company = {"name": i[0], "sector": i[1], "type": i[2]}
        Company(**company).save_to_db()

    # Insert all users from  "static/liste_apprenants.csv"
    with open("App/static/seed/liste_apprenants.csv", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)

    for i in data:
        print(i)
        user = {
            "email": i[0],
            "first_name": i[1],
            "last_name": i[2],
            "password": generate_password_hash(i[3], method="sha256"),
            "is_admin": i[4]  # True if i[4] == "TRUE" else False
            #'create_time': 00
        }
        User(**user).save_to_db()

    # Create candidacies from users and companies
    # with open("App/static/seed/candidacies.csv", newline='') as f:
    #     reader = csv.reader(f)
    #     next(reader)
    #     data = list(reader)
    # for i in data:
    #     candidacy = {
    #         "user_id": i[0],
    #         "company_id": i[1],
    #         "contact_full_name": i[2],
    #         "contact_email": i[3],
    #         "date": i[4],
    #         "contact_phone": i[5],
    #         "status": i[6],
    #         "job_title": i[7],
    #         "contact_link": i[8],
    #         "location_id": i[9]
    #     }
    #     Candidacy(**candidacy).save_to_db()

    lg.warning("Database initialized!")
