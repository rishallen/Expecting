from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")


    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from app.models.provider import Provider
    from app.models.address import Address
    from app.models.user import User
    from app.models.login import Login
    from app.models.post import Post

    from .routes import address_bp
    app.register_blueprint(address_bp)

    from .routes import provider_bp
    app.register_blueprint(provider_bp)

    from .routes import user_bp
    app.register_blueprint(user_bp)

    from .routes import login_bp
    app.register_blueprint(login_bp)

    from .routes import post_bp
    app.register_blueprint(post_bp)

    CORS(app)
    return app
