from App import db

class Location(db.Model):
    __tablename__ = "location"

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
