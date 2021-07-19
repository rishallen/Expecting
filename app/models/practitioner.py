from app import db

class Practitioner (db.Model):
    practitioner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    title = db.Column(db.String)
    social_media_handle = db.Column(db.String)
    description = db.Column(db.String)
    addresses = db.relationship('Address', backref='address', lazy=True)

