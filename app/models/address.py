from app import db

class Address (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postal_code = db.Column(db.String)
    street_name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('practitioner.practitioner_id'), nullable=True)