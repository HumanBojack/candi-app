from App import db

class Company(db.Model):
    __tablename__ = "company"

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