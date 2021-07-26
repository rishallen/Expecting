from flask import Blueprint, request, jsonify, make_response
from app import db
from dotenv import load_dotenv
from app.models.post import Post
from app.models.provider import Provider
from app.models.address import Address
from app.models.user import User

import os

load_dotenv()

provider_bp = Blueprint('provider', __name__)
address_bp = Blueprint('address', __name__)
user_bp = Blueprint('user', __name__ )
login_bp = Blueprint('login', __name__ )
post_bp = Blueprint('post', __name__ )

@provider_bp.route('/')
def root():
    return {
        "name":"expecting"
    }

# Provider routes
# Get all providers
@provider_bp.route('/providers', methods=["GET", "POST"], strict_slashes = False)
def handle_providers():
    if request.method == "GET":
        providers = Provider.query.all()

        providers_response = []
        for provider in providers:
            providers_response.append(Provider.response_dict(provider))
        return jsonify(providers_response)

    # Create new provider
    elif request.method == "POST":
        request_body = request.get_json()
        first_name = request_body.get("first_name")
        last_name = request_body.get("last_name")
        title = request_body.get("title")
        social_media_handle = request_body.get("social_media_handle")
        description =  request_body.get("description")
        address = request_body.get("address")
        post = request_body.get("post")
        user_id = request_body.get("user_id")

        if ("first_name" not in request_body or 
            "last_name"not in request_body or 
            "title" not in request_body or 
            "social_media_handle" not in request_body or 
            "description" not in request_body or 
            "address" not in request_body):
            # "user_id" not in request_body
            
            
            return jsonify({"details": "Invalid data"}), 400

        new_provider = Provider(first_name=first_name,
                        last_name=last_name,
                        title=title,
                        social_media_handle=social_media_handle,
                        description=description,
                        user_id=user_id)

        db.session.add(new_provider)
        db.session.commit()

        
        if "postal_code" not in address or "street_name" not in address or "city" not in address or "state" not in address or "country" not in address:
            return jsonify({"details": "Invalid data"}), 400
        new_address = Address(postal_code=address["postal_code"],
                            street_name=address["street_name"],
                            city=address["city"],
                            state=address["state"],
                            country=address["country"],
                            provider_id= new_provider.provider_id)


        db.session.add(new_address)
        db.session.commit()

        
        registered_provider = {"provider":
            Provider.response_dict(new_provider)}
        return jsonify(registered_provider), 201


@provider_bp.route("/providers/<provider_id>", methods=["GET", "PATCH", "DELETE"])
def handle_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    if request.method == "GET":
        selected_provider = {"provider":
        Provider.response_dict(provider)}
        return jsonify(selected_provider),200

    # Update a provider
    elif request.method == "PATCH":
        provider_data = request.get_json()
        provider.update_from_dict(provider_data)

        db.session.commit()
        response_body = {
            "provider": provider.response_dict()
        }
        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(provider)
        db.session.commit()
        provider_response_body = {"details": f'provider number {provider.provider_id} "{provider.title}" successfully deleted'}
        return jsonify(provider_response_body),200

# Posts route:
# Get Posts       
@provider_bp.route("/providers/<provider_id>/users/<user_id>/posts", methods=["GET","POST"])
def handle_posts(provider_id, user_id):
    provider = Provider.query.get_or_404(provider_id)
    

    if request.method == "GET":
        posts = provider.posts
        posts_response = []
        for post in posts:
            if str(post.user_id) == user_id:
                posts_response.append({
                "post_id": post.post_id,
                "message": post.message,
                "provider_id": post.provider_id,
                "user_id": post.user_id
        })
        return jsonify(posts_response)

    # Create post route:
    elif request.method == "POST":
        request_body = request.get_json()
        user = User.query.get_or_404(user_id)

        if "message" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_post = Post(message=request_body["message"], provider_id=provider.provider_id, user_id=user.user_id)
        db.session.add(new_post)
        db.session.commit()
        
        commited_post = {"post": {
            "post_id": new_post.post_id,
            "message": new_post.message,
            # "votes": new_post.like_count,
            # put the provider is there is one
            "provider_id": new_post.provider_id,
            "user_id": new_post.user_id
        }}
        return jsonify(commited_post), 201

# Votes route:
@post_bp.route("/<post_id>/votes", methods=["PATCH"])
def handle_post_like(post_id):
    post = Post.query.get_or_404(post_id)
    vote = request.args.get("like_count")
    post.like_count += int(vote)

    db.session.commit()
    response_body = {
        "post": {
            "post_id": post.post_id,
            "message": post.message,
            "votes": post.like_count,
        }
    }
    return jsonify(response_body), 200

@post_bp.route("/posts/<post_id>", methods=["DELETE"])
def handle_post_del(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    posts_response_body = {"details": f'post {post.post_id} "{post.message}" successfully deleted'}
    return jsonify(posts_response_body),200

# User route
@user_bp.route("/users", methods=["GET", "POST"])
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


@login_bp.route('/login', methods=["POST"])
def handle_login():
    # if request.method == "GET":
    #     logins = Login.query.all()

    #     logins_response = []
    #     for login in logins:
    #         logins_response.append(Login.login_dict(login))
    #     return jsonify(logins_response)

        request_body = request.get_json()
        username = request_body.get("username")
        password = request_body.get("password")

        if "username" not in request_body or "password" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        logged_in_user = User.query.filter_by(username=username,
                                password=password).one_or_none()
        if logged_in_user is None:
            return jsonify({"details": "log in failed"}), 404

        result_login={"user":
            logged_in_user.user_dict()}
        return jsonify(result_login), 200

# Adresses route
# Add additional address 
@address_bp.route("/providers/<provider_id>/address", methods = ["POST", "GET"], strict_slashes = False)
def handle_address(provider_id):
    provider = Provider.query.get(provider_id)

    if request.method == "GET":
        address = provider.address
        address_response = []
        address_response.append(Address.address_response_dict(address))
        return jsonify(address_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "postal_code" not in request_body or "recipient" not in request_body or "street_name" not in request_body or "city" not in request_body or "state" not in request_body or "country" not in request_body or "provider_id" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        

    