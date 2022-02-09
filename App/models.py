from App import db, login_manager
import datetime 
from flask_login import UserMixin # allow to set variable is_active=True and to stay connected
import logging as lg
from werkzeug.security import generate_password_hash
import csv
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    """Allow to create a current_user with his id

    Args:
        user_id (int): user_id from the database

    Returns:
        instance of users depending of his id
    """
    return User.query.get(int(user_id))

# coding: utf-8
class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_by_id(cls, location_id):
        return cls.query.filter_by(id=location_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
class User(db.Model,UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.String(), default=datetime.date.today())
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    is_admin =db. Column(db.Integer, nullable=False, default=0)
    promotion = db.Column(db.String(45), nullable=True)
    
    def __repr__(self):
        return f'{self.last_name} {self.first_name}'

    def json(self):
        return {
            'id' : self.id,
            'email' :self.email,
            'password' : self.password,
            'create_time' : self.create_time,
            'first_name' : self.first_name,
            'last_name' :self.last_name,
            'phone_number': self.phone_number,
            'is_admin' : self.is_admin,
            'promotion' : self.promotion
            }
     
    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    sector = db.Column(db.Integer, nullable=False, default=0)
    type = db.Column(db.Integer, nullable=False)
    
    @classmethod
    def find_by_id(cls, company_id):
        return cls.query.filter_by(id=company_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
class Candidacy(db.Model):
    __tablename__ = 'candidacy'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    company_id = db.Column(db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False, index=True)
    location_id = db.Column(db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False, index=True)
    contact_full_name = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(), default=datetime.date.today())
    contact_phone = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, default=0)
    job_title = db.Column(db.Integer, nullable=False, default=0)
    contact_link = db.Column(db.String(255), nullable=True)

    location = relationship('Location')
    company = relationship('Company')
    user = relationship('User')
    
    @classmethod
    def find_by_user_id(cls, user_id):
        candidacy_list=[]
        for candidacy in cls.query.filter_by(user_id=user_id).all():
            candidacy_list.append(candidacy.json())
        return candidacy_list
    
    @classmethod
    def get_all_in_list_with_user_name(cls):
        candidacy_list=[]
        for candidacy in cls.query.join(User).with_entities(User.first_name, cls.contact_full_name, User.email, cls.contact_phone, cls.date, cls.status).all():
            candidacy_list.append(candidacy)
        return candidacy_list
    
    @classmethod
    def find_by_id(cls, candidacy_id):
        return cls.query.filter_by(id=candidacy_id).first()

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_id": self.company_id,
            "location_id": self.location_id,
            "contact_full_name": self.contact_full_name,
            "contact_email": self.contact_email,
            "date": self.date,
            "contact_phone": self.contact_phone,
            "status": self.status,
            "job_title": self.job_title,
            "contact_link": self.contact_link
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
 
# Function to create db and populate it
def init_db():
    db.drop_all()
    db.create_all()

def seed_db():
    User(email= "cb@gmail.com", password = generate_password_hash("1234", method='sha256'), last_name="ben", first_name= "charles", is_admin=True).save_to_db() 
    User(email= "bb@gmail.com", password = generate_password_hash("1234", method='sha256'), last_name="beniac", first_name= "cha", is_admin=False, promotion='Dev IA').save_to_db()

    # Import and creates regions
    with open("App/static/seed/regions.csv", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        regions_data = list(reader)
    for region in regions_data:
        location = {
            "region": region[0]
        }
        Location(**location).save_to_db()
    
    # Import and create companies
    with open("App/static/seed/companies.csv", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        companies_data = list(reader)
    for i in companies_data:
        company = {
            "name": i[0],
            "sector": i[1],
            "type": i[2]
            # "location_id": i[3]
        }
        Company(**company).save_to_db()

    # # Import and create jointable between locations and companies
    # with open("App/static/seed/locationcompanyjt.csv", newline='') as f:
    #     reader = csv.reader(f)
    #     next(reader)
    #     data = list(reader)
    #     for i in data:
    #         jt_element = {
    #             "location_id": i[0], 
    #             "company_id": i[1]
    #         }
    #         LocationCompanyJt(**jt_element).save_to_db()
    
    # Insert all users from  "static/liste_apprenants.csv"
    with open("App/static/seed/liste_apprenants.csv", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)

    for i in data:
        print(i)
        user = {
                'email' : i[0],
                'first_name' : i[1],
                'last_name' : i[2],
                'password' : generate_password_hash(i[3], method='sha256'),
                'is_admin' : True if i[4] == "TRUE" else False
                #'create_time': 00
            }
        User(**user).save_to_db()

    # Create candidacies from users and companies
    with open("App/static/seed/candidacies.csv", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)
    for i in data:
        candidacy = {
            "user_id": i[0],
            "company_id": i[1],
            "contact_full_name": i[2],
            "contact_email": i[3],
            "date": i[4],
            "contact_phone": i[5],
            "status": i[6],
            "job_title": i[7],
            "contact_link": i[8],
            "location_id": i[9]
        }
        Candidacy(**candidacy).save_to_db()
    
    lg.warning('Database initialized!')
