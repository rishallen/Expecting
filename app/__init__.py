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
    # from app.models.card import Card
    from app.models.practitioner import Practitioner
    from app.models.address import Address

    from .routes import address_bp
    app.register_blueprint(address_bp)

    from .routes import practitioner_bp
    app.register_blueprint(practitioner_bp)

    CORS(app)
    return app
