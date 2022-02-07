from App import db,login_manager
import datetime 
from flask_login import UserMixin # allow to set variable is_active=True and to stay connected
import logging as lg
from werkzeug.security import generate_password_hash
import csv
from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

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
    is_admin =db. Column(db.Integer, nullable=False, server_default=text("'0'"))
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
        return cls.query.filter_by(id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sector = db.Column(db.Integer, nullable=False, server_default=text("'0'"))
    type = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False, index=True)

    location = relationship('Location')
    
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
    company_id = db.Column(db.ForeignKey('company.id'), nullable=False, index=True)
    contact_full_name = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(), default=datetime.date.today())
    contact_phone = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, server_default=text("'0'"))
    job_title = db.Column(db.Integer, nullable=False, server_default=text("'0'"))
    contact_link = db.Column(db.String(255), nullable=True)
    location_id = db.Column(db.Integer, nullable=False)

    company = relationship('Company')
    user = relationship('User')
    
    @classmethod
    def find_by_id(cls, candidacy_id):
        return cls.query.filter_by(id=candidacy_id).first()

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
    #db.session.add( )
    User(email= "cb@gmail.com", password = generate_password_hash("1234", method='sha256'), last_name="ben", first_name= "charles", is_admin=True).save_to_db() 
    User(email= "bb@gmail.com", password = generate_password_hash("1234", method='sha256'), last_name="beniac", first_name= "cha", is_admin=False, promotion='Dev IA').save_to_db()


