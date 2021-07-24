from app import db

class Post (db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


    def post_response_dict(post):
        return {
            "post_id": post.post_id,
            "message": post.message,
            "user_id": post.user_id,
            "provider_id": post.provider_id
        }