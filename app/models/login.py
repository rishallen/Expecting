from app import db

class Login (db.Model):
    username = db.Column(db.String, primary_key=True,)
    password = db.Column(db.String)

    def login_dict(self):
        return {
            # "login_id": self.login_id,
            "username": self.username,
            "password": self.password
        }