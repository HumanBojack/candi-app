from App import db, login_manager
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """Allow to create a current_user with his id

    Args:
        user_id (int): user_id from the database

    Returns:
        instance of users depending of his id
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.String(), default=datetime.date.today())
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    promotion = db.Column(db.String(45), nullable=True)

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "create_time": self.create_time,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "is_admin": self.is_admin,
            "promotion": self.promotion,
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