from app.api import bp
from app.models import User, Ticket
from flask import jsonify, request
from app.api.auth import token_auth
from app import db


@bp.route('/users/<int:user_id>/tickets', methods=['GET'])
@token_auth.login_required
def get_user_tickets(user_id):
    user_tickets = User.query.filter_by(id=user_id).first().assigned_tickets
    user_tickets_for_json = [
        {
            "flight_id": ticket.flight_id,
            "type": ticket.type,
            "price": float(ticket.price),
            "luggages": [
                {
                    'id': luggage.id,
                    'type_id': luggage.type_id,
                    'price':float(luggage.price)
                } for luggage in ticket.assigned_luggages
            ]
        } for ticket in user_tickets
    ]

    return jsonify(user_tickets_for_json)

@bp.route('/users/<int:user_id>/tickets/<int:ticket_id>', methods=['GET'])
@token_auth.login_required
def get_user_ticket_by_ticket_id(user_id, ticket_id):
    user_tickets = User.query.filter_by(id=user_id).first().assigned_tickets
    for ticket in user_tickets:
        if ticket.id == ticket_id:
            return jsonify(
                    flight_id = ticket.flight_id,
                    type_id = ticket.type,
                    price = float(ticket.price),
                    luggages = [
                            {
                                'id': luggage.id,
                                'type_id': luggage.type_id,
                                'price':float(luggage.price)
                            } for luggage in ticket.assigned_luggages
                    ]
            )
    return jsonify(message="not found")

@bp.route('/users/<int:user_id>/tickets', methods=['POST'])
@token_auth.login_required
def create_user_ticket(user_id):
    data = request.get_json(force=True)
    ticket = Ticket(
        price=float(data["price"]),
        flight_id=data["flight_id"],
        type_id=data["type_id"],
        user_id=user_id
    )
    db.session.add(ticket)
    db.session.commit()
    ticket = Ticket.query.filter_by(id=ticket.id).first()
    return jsonify(
        id=ticket.id,
        price=float(ticket.price),
        flight_id=ticket.flight_id,
        type_id=ticket.type_id,
        user_id=ticket.user_id
    )

@bp.route('tickets/<int:ticket_id>', methods=['PUT'])
@token_auth.login_required
def update_user_flight(ticket_id):
    data = request.get_json(force=True)
    Ticket.query.filter_by(id=ticket_id).update(
        {
        Ticket.price: data["price"],
        Ticket.flight_id: data["flight_id"],
        Ticket.type_id: data["type_id"],
        Ticket.user_id: data["user_id"]
        }
    )
    db.session.commit()
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    return jsonify(
        id=ticket.id,
        price=float(ticket.price),
        flight_id=ticket.flight_id,
        type_id=ticket.type_id,
        user_id=ticket.user_id
    )

@bp.route('tickets/<int:ticket_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user_flight(ticket_id):
    Ticket.query.filter_by(id=ticket_id).delete()
    db.session.commit()
    return jsonify(
        message="success"
    )

