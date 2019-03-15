from collections import namedtuple
from app.api import bp
from app.models import User

from flask import jsonify, request
from app import db


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    roles = [
        {
            "role": user.role.name
        }
    ]
    user_tickets = namedtuple(
        'UserTickets', [
            'user',
            'price',
            'date_dep',
            'date_ar',
            'from_',
            'to_'
        ]
    )
    tickets_for_json = []
    for ticket in map(user_tickets._make, user.user_flights):
        tickets_for_json.append(
            {
                'from': ticket.from_,
                'to': ticket.to_,
                'date_of_departure': ticket.date_dep,
                'date_of_arrival': ticket.date_ar
            }
        )

    return jsonify(
        id=user.id,
        username=user.username,
        roles=roles,
        tickets=tickets_for_json
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
