from app import db

class Address (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postal_code = db.Column(db.String)
    street_name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('practitioner.practitioner_id'), nullable=True)

    def address_response_dict(address):
        return {
            "postalCode": address.postal_code,
            "street": address.street_name,
            "city": address.city,
            "state": address.state,
            "country": address.country
        }
    

    def update_from_dict(self, data):
        self.postal_code=data["postalCode"]
        self.street_name=data["street"]
        self.city=data["city"]
        self.state=data["state"]
        self.country=data["country"]