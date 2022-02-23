from secrets import token_urlsafe

from flask import jsonify, request

from app.configs.database import db
from app.models.user_model import UserModel
from app.configs.auth import auth


def register_user():
    data = request.get_json()
    data["api_key"] = token_urlsafe(16)

    user = UserModel(**data)

    db.session.add(user)
    db.session.commit()

    return jsonify(user), 201

def login_user():
    data = request.get_json()

    user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    if not user:
        return {"error": "email not found"}, 401

    if not user.check_password(data["password"]):
        return {"error": "email and password missmatch"}, 401
    
    token = user.api_key

    return {"api_key": token}, 200

@auth.login_required
def get_user():
    return jsonify(auth.current_user()), 200

@auth.login_required
def update_user():
    data = request.get_json()

    user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    for key, value in data.items():
        setattr(user, key, value)

    db.session.add(user)
    db.session.commit()

    return jsonify(user), 200

@auth.login_required
def delete_user():
    email_to_del = auth.current_user().email

    user: UserModel = UserModel.query.filter_by(email=email_to_del).first()

    db.session.delete(user)
    db.session.commit()

    return {"msg": f"User {user.name} has been deleted"}