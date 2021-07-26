from app import db
from app.models.address import Address
from app.models.post import Post

class Provider (db.Model):
    provider_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    title = db.Column(db.String)
    social_media_handle = db.Column(db.String)
    description = db.Column(db.String)
    address = db.relationship('Address', backref='provider', uselist=False, lazy=True)
    posts = db.relationship('Post', backref='provider', lazy=True, order_by="Post.post_id")
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


    def response_dict(provider):
        return {
            "provider_id": provider.provider_id,
            "first_name": provider.first_name,
            "last_name": provider.last_name,
            "title": provider.title,
            "social_media_handle": provider.social_media_handle,
            "description": provider.description,
            "address": Address.address_response_dict(provider.address),
            "user_id": provider.user_id

        }
    
    def update_from_dict(self, data):
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.title=data["title"]
        self.social_media_handle=data["social_media_handle"]
        self.description=data["description"]
        self.address.update_from_dict(data["address"])

        # provider_data.items():
        #     if k != 'address':
        #         setattr(provider, k, v)
        # address_data = provider_data["address"]
        # address = provider.address
        # for k, v in address_data.items():
        #     setattr(address, k, v)