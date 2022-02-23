from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from app.configs.auth import auth
from app.configs.database import db
from app.models.user_model import UserModel


def register_user():
    data = request.get_json()

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
    
    token = create_access_token(user)

    return {"token": token}, 200

@jwt_required()
def get_user():
    return jsonify(get_jwt_identity()), 200

@jwt_required()
def update_user():
    data = request.get_json()

    user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    for key, value in data.items():
        setattr(user, key, value)

    db.session.add(user)
    db.session.commit()

    return jsonify(user), 200

@jwt_required()
def delete_user():
    email_to_del = get_jwt_identity()['email']

    user: UserModel = UserModel.query.filter_by(email=email_to_del).first()

    db.session.delete(user)
    db.session.commit()

    return {"msg": f"User {user.name} has been deleted"}