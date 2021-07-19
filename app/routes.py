from flask import Blueprint, request, jsonify, make_response
from app import db
from dotenv import load_dotenv
from app.models.practitioner import Practitioner
from app.models.address import Address
import os

load_dotenv()

practitioner_bp = Blueprint('practitioner', __name__)
address_bp = Blueprint('address', __name__)

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
            practitioners_response.append({
                "practitioner_id": practitioner.practitioner_id,
                "first_name": practitioner.first_name,
                "last_name": practitioner.last_name,
                "title": practitioner.title,
                "social_media_handle": practitioner.social_media_handle,
                "description": practitioner.description
            })
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
        
        subscribed_practitioner = {"practitioner":
            {"practitioner_id": new_practitioner.practitioner_id,
            "FirstName": new_practitioner.first_name,
            "LastName": new_practitioner.last_name,
            "Title": new_practitioner.title,
            "Social_media_handle": new_practitioner.social_media_handle
        }}
        return jsonify(subscribed_practitioner), 201 

# Delete Practitioner
@practitioner_bp.route("/practitioners/<practitioner_id>", methods=["GET", "DELETE"])
def handle_practitioner(practitioner_id):
    practitioner = Practitioner.query.get_or_404(practitioner_id)
    if request.method == "GET":
        selected_practitioner = {"practitioner":
        {"practitioner_id": practitioner.practitioner_id,
        "FirstName": practitioner.first_name,
        "LastName": practitioner.last_name,
        "Title": practitioner.title,
        "Social_media_handle": practitioner.social_media_handle,
        "Description": practitioner.description
        }}
        return jsonify(selected_practitioner),200
    elif request.method == "DELETE":
        db.session.delete(practitioner)
        db.session.commit()
        practitioner_response_body = {"details": f'practitioner number {practitioner.practitioner_id} "{practitioner.title}" successfully deleted'}
        return jsonify(practitioner_response_body),200


# Adresses route
# Add additional addresses 
@address_bp.route("/practitioners/<practitioner_id>/addresses", methods = ["POST", "GET"], strict_slashes = False)
def handle_addresses(practitioner_id):
    practitioner = Practitioner.query.get(practitioner_id)

    if request.method == "GET":
        addresses = practitioner.addresses
        addresses_response = []
        for address in addresses:
            addresses_response.append({
            "postalCode": address.postal_code,
            "recipient": address.recipient,
            "street": address.street_name,
            "city": address.city,
            "state": address.state,
            "country": address.country,
            "practitioner_id": address.practitioner_id,
        })
        return jsonify(addresses_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "postal_code" not in request_body or "recipient" not in request_body or "street_name" not in request_body or "city" not in request_body or "state" not in request_body or "country" not in request_body or "practitioner_id" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        

    