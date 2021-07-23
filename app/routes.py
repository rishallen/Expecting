from flask import Blueprint, request, jsonify, make_response
from app import db
from dotenv import load_dotenv
from app.models.practitioner import Practitioner
from app.models.address import Address
from app.models.user import User
from app.models.login import Login

import os

load_dotenv()

practitioner_bp = Blueprint('practitioner', __name__)
address_bp = Blueprint('address', __name__)
user_bp = Blueprint('user', __name__ )
login_bp = Blueprint('login', __name__ )

@practitioner_bp.route('/')
def root():
    return {
        "name":"mango-mania"
    }

# Practitioner routes
# Get all practitioners
@practitioner_bp.route('/practitioners', methods=["GET", "POST"], strict_slashes = False)
def handle_practitioners():
    if request.method == "GET":
        practitioners = Practitioner.query.all()

        practitioners_response = []
        for practitioner in practitioners:
            practitioners_response.append(Practitioner.response_dict(practitioner))
        return jsonify(practitioners_response)

    # Create new practitioner
    elif request.method == "POST":
        request_body = request.get_json()
        first_name = request_body.get("FirstName")
        last_name = request_body.get("LastName")
        title = request_body.get("Title")
        social_media_handle = request_body.get("Social_media_handle")
        description =  request_body.get("Description")
        address = request_body.get("address")

        if "FirstName" not in request_body or "LastName" not in request_body or "Title" not in request_body or "Social_media_handle" not in request_body or "Description" not in request_body or "address" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        new_practitioner = Practitioner(first_name=first_name,
                        last_name=last_name,
                        title=title,
                        social_media_handle=social_media_handle,
                        description=description)
        db.session.add(new_practitioner)
        db.session.commit()

        
        if "postalCode" not in address or "street" not in address or "city" not in address or "state" not in address or "country" not in address:
            return jsonify({"details": "Invalid data"}), 400
        new_address = Address(postal_code=address["postalCode"],
                            street_name=address["street"],
                            city=address["city"],
                            state=address["state"],
                            country=address["country"],
                            practitioner_id= new_practitioner.practitioner_id)

        db.session.add(new_address)
        db.session.commit()
        
        registered_practitioner = {"practitioner":
            Practitioner.response_dict(new_practitioner)}
        return jsonify(registered_practitioner), 201


@practitioner_bp.route("/practitioners/<practitioner_id>", methods=["GET", "PATCH", "DELETE"])
def handle_practitioner(practitioner_id):
    practitioner = Practitioner.query.get_or_404(practitioner_id)
    if request.method == "GET":
        selected_practitioner = {"practitioner":
        Practitioner.response_dict(practitioner)}
        return jsonify(selected_practitioner),200

    # Update a practitioner
    elif request.method == "PATCH":
        practitioner_data = request.get_json()
        practitioner.update_from_dict(practitioner_data)

        db.session.commit()
        response_body = {
            "practitioner": practitioner.response_dict()
        }
        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(practitioner)
        db.session.commit()
        practitioner_response_body = {"details": f'practitioner number {practitioner.practitioner_id} "{practitioner.title}" successfully deleted'}
        return jsonify(practitioner_response_body),200

# User route
@user_bp.route("/register", methods=["GET", "POST"])
def handle_user():
    if request.method == "GET":
        users = User.query.all()

        users_response = []
        for user in users:
            users_response.append(user.user_dict())
        return jsonify(users_response)

    elif request.method == "POST":
        request_body = request.get_json()
        username = request_body.get("username")
        password = request_body.get("password")
        email = request_body.get("email")

        if "username" not in request_body or "password" not in request_body or "email" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        registered_user = User(username=username,
                            password=password,
                            email=email)
        db.session.add(registered_user)
        db.session.commit()

        result_user={"user":
            User.user_dict(registered_user)}
        
        return jsonify(result_user), 201


@login_bp.route('/login', methods=["GET", "POST"])
def handle_login():
    if request.method == "GET":
        logins = Login.query.all()

        logins_response = []
        for login in logins:
            logins_response.append(Login.login_dict(login))
        return jsonify(logins_response)

    elif request.method == "POST":
        request_body = request.get_json()
        username = request_body.get("username")
        password = request_body.get("password")

        if "username" not in request_body or "password" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        registered_login = Login(username=username,
                            password=password)
        # db.session.add(registered_login)
        # db.session.commit()

        result_login={"login":
            Login.login_dict(registered_login)}
        
        return jsonify(result_login), 201

# Adresses route
# Add additional address 
@address_bp.route("/practitioners/<practitioner_id>/address", methods = ["POST", "GET"], strict_slashes = False)
def handle_address(practitioner_id):
    practitioner = Practitioner.query.get(practitioner_id)

    if request.method == "GET":
        address = practitioner.address
        address_response = []
        address_response.append(Address.address_response_dict(address))
        return jsonify(address_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "postal_code" not in request_body or "recipient" not in request_body or "street_name" not in request_body or "city" not in request_body or "state" not in request_body or "country" not in request_body or "practitioner_id" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        

    