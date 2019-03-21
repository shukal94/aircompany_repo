from app.api import bp
from app.models import User

from flask import jsonify, request
from app import db


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()

    return jsonify(
        id=user.id,
        username=user.username,
        role=user.role.name,
        flights=[
            {
                'from': flight._from,
                'to': flight._to,
                'date_departure': flight.date_departure,
                'date_arrival': flight.date_arrival
            }
            for flight in user.assigned_flights
        ]
    )


@bp.route('/users', methods=['GET'])
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
def create_user():
    data = request.get_json(force=True)
    user = User(
        username=data["username"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        address=data["address"],
        postal_code=data["postal_code"]
    )
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username=user.username).first()
    return jsonify(
        id=user.id,
        username=user.username
    )


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass


@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass
