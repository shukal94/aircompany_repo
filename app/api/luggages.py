from app.api import bp
from app.models import Luggage, Ticket

from flask import jsonify, request
from app import db
from app.api.auth import token_auth

@bp.route('/tickets/<int:id>/luggages', methods=['GET'])
@token_auth.login_required
def get_luggage(id):
    ticket = Ticket.query.filter_by(id=id).first()
    return jsonify(
        [{'id':luggage.id,
        'type_id':luggage.type_id,
        'ticket_id':luggage.ticket_id,
        'price':float(luggage.price)} for luggage in ticket.assigned_luggages] )

@bp.route('/tickets/<int:id>/luggages', methods=['POST'])
@token_auth.login_required
def create_luggage(id):
    data = request.get_json(force=True)
    luggage = Luggage(
        type_id=data["type_id"],
        ticket_id=data["ticket_id"],
        price=data["price"]
        )
    db.session.add(luggage)
    db.session.commit()
    Luggage.query.filter_by(id=id).first()
    return jsonify(
        id=luggage.id,
        type_id=luggage.type_id,
        ticket_id=luggage.ticket_id,
        price=float(luggage.price)
    )

@bp.route('/luggages/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_luggage(id):
    data = request.get_json(force=True)
    Luggage.query.filter_by(id=id).update(
        {
            Luggage.type_id:data["type_id"],
            Luggage.ticket_id:data["ticket_id"],
            Luggage.price:data["price"]
        }
    )
    db.session.commit()
    luggage = Luggage.query.filter_by(id=id).first()
    return jsonify(
        id=luggage.id,
        type_id=luggage.type_id,
        ticket_id=luggage.ticket_id,
        price=float(luggage.price)
    )

@bp.route('/luggages/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_luggage(id):
    Luggage.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(
        message="success"
    )
