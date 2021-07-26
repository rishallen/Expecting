from app import db

class User (db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    provider = db.relationship('Provider', backref='user', uselist=False, lazy=True)

    def user_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "provider_id": self.provider.provider_id if self.provider else None
        }
    