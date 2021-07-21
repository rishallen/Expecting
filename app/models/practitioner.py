from app import db
from app.models.address import Address

class Practitioner (db.Model):
    practitioner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    title = db.Column(db.String)
    social_media_handle = db.Column(db.String)
    description = db.Column(db.String)
    address = db.relationship('Address', backref='address', uselist=False, lazy=True)

    def response_dict(practitioner):
        return {
            "practitioner_id": practitioner.practitioner_id,
            "first_name": practitioner.first_name,
            "last_name": practitioner.last_name,
            "title": practitioner.title,
            "social_media_handle": practitioner.social_media_handle,
            "description": practitioner.description,
            "address": Address.address_response_dict(practitioner.address)
        }