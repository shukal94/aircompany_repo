from app.api import bp
from app.models import User

from flask import jsonify, request
from app import db
from app.api.auth import token_auth


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(
        id=user.id,
        username=user.username,
        role=user.role.name,
        postal_code=user.postal_code,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        state=user.state,
        country=user.country,
        email=user.email,
        about_me=user.about_me,        
        flights=[{
                    'from': flight._from,
                    'to': flight._to,
                    'date_departure': flight.date_departure,
                    'date_arrival': flight.date_arrival
                } for flight in user.assigned_flights]
    )


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    users = User.query.select_from().all()
    users_to_json = [
        {
            "id": user.id,
            "username": user.username
        }
        for user in users
    ]
    return jsonify(users_to_json)


@bp.route('/users', methods=['POST'])
@token_auth.login_required
def create_user():
    data = request.get_json(force=True)
    user = User(
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        address=data["address"],
        postal_code=data["postal_code"],
        email=data["email"],
        country=data["country"],
        state=data["state"],
        about_me=data["about_me"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username=user.username).first()
    return jsonify(
        id=user.id,
        username=user.username,
        postal_code=user.postal_code,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        state=user.state,
        country=user.country,
        email=user.email,
        about_me=user.about_me,
        role_id=user.role_id
    )


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    data = request.get_json(force=True)
    User.query.filter_by(id=id).update(
        {
            User.postal_code: data["postal_code"],
            User.username: data["username"],
            User.first_name: data["first_name"],
            User.last_name: data["last_name"],
            User.address: data["address"],
            User.state: data["state"],
            User.country: data["country"],
            User.email: data["email"],
            User.about_me: data["about_me"],
            User.role_id: data["role_id"]
        }
    )
    db.session.commit()
    user = User.query.filter_by(id=id).first()
    return jsonify(
        id=user.id,
        username=user.username,
        postal_code=user.postal_code,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        state=user.state,
        country=user.country,
        email=user.email,
        about_me=user.about_me,
        role_id=user.role_id
    )


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(
        message="success"
    )
