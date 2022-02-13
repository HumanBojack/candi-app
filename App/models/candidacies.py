from App import db
from App.models.companies import Company
from App.models.users import User
from App.static import constant
import datetime
from sqlalchemy.orm import relationship

class Candidacy(db.Model):
    __tablename__ = "candidacy"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(
        db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company_id = db.Column(
        db.ForeignKey("company.id", ondelete="CASCADE"), nullable=False, index=True
    )
    location_id = db.Column(
        db.ForeignKey("location.id", ondelete="CASCADE"), nullable=False, index=True
    )
    contact_full_name = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, default=datetime.date.today())  # db.DateTime ?
    contact_phone = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, default=0)
    job_title = db.Column(db.Integer, nullable=False, default=0)
    contact_link = db.Column(db.String(255), nullable=True)

    location = relationship("Location")
    company = relationship("Company")
    user = relationship("User")

    @classmethod
    def find_by_user_id(cls, user_id):
        candidacy_list = []
        for candidacy in cls.query.filter_by(user_id=user_id).all():
            candidacy_list.append(candidacy.json())
        return candidacy_list

    @classmethod
    def user_to_json(cls, id):
        candidacies = []
        for candidacy in cls.query.filter_by(user_id=id).all():
            candidacy_js = candidacy.json()
            candidacy_js[
                "user"
            ] = f"{candidacy.user.first_name} {candidacy.user.last_name}"
            candidacy_js["company"] = candidacy.company.name
            candidacy_js["location"] = candidacy.location.region
            candidacy_js["status_interpreted"] = constant.STATUS[int(candidacy.status)][
                1
            ]
            candidacy_js["job_title_interpreted"] = constant.JOB_TITLES[
                int(candidacy.job_title)
            ][1]
            candidacies.append(candidacy_js)
        return candidacies

    @classmethod
    def all_candidacies_to_list(cls):
        candidacy_list = []
        for candidacy in (
            cls.query.join(User, Company)
            .with_entities(
                User.first_name,
                User.last_name,
                User.email,
                cls.contact_full_name,
                cls.contact_phone,
                Company.name,
                cls.date,
                cls.status,
                cls.job_title,
            )
            .all()
        ):
            item = dict(candidacy)
            item["status"] = constant.STATUS[int(candidacy.status)][1]
            item["job_title"] = constant.JOB_TITLES[int(candidacy.job_title)][1]
            candidacy_list.append(item)
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
            "contact_link": self.contact_link,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()