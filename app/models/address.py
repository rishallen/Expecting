from app import db

class Address (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postal_code = db.Column(db.String)
    street_name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'), nullable=True)

    def address_response_dict(address):
        return {
            "postal_code": address.postal_code,
            "street_name": address.street_name,
            "city": address.city,
            "state": address.state,
            "country": address.country
        }
    

    def update_from_dict(self, data):
        self.postal_code=data["postal_code"]
        self.street_name=data["street_name"]
        self.city=data["city"]
        self.state=data["state"]
        self.country=data["country"]
