from app.api import bp
from app.models import Flight

from flask import jsonify, request
from app import db
from app.api.auth import token_auth

@bp.route('/flights/<int:id>', methods=['GET'])
@token_auth.login_required
def get_flight(id):
    flight = Flight.query.filter_by(id=id).first()

    return jsonify(
        id=flight.id,
        _from=flight._from,
        _to=flight._to,
        date_departure=flight.date_departure,
        date_arrival=flight.date_arrival,
        tickets=[{
                    'type': ticket.type,
                    'user_id': ticket.user_id,
                } for ticket in flight.assigned_tickets
        ]
    )

@bp.route('/flights', methods=['GET'])
@token_auth.login_required
def get_flights():
    flights = Flight.query.select_from().all()
    flights_to_json = [
        {
            'id': flight.id,
            '_from': flight._from,
            '_to': flight._to,
            'date_departure': flight.date_departure,
            'date_arrival': flight.date_arrival
        }
        for flight in flights
    ]
    return jsonify(flights_to_json)

@bp.route('/flights', methods=['POST'])
@token_auth.login_required
def create_flight():
    data = request.get_json(force=True)
    flight = Flight(
        _from=data["_from"],
        _to=data["_to"],
        date_departure=data["date_departure"],
        date_arrival=data["date_arrival"]
    )
    db.session.add(flight)
    db.session.commit()
    flight = Flight.query.filter_by(id=flight.id).first()
    return jsonify(
        id=flight.id,
        _from=flight._from,
        _to=flight._to,
        date_departure=flight.date_departure,
        date_arrival=flight.date_arrival)


@bp.route('/flights/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_flight(id):
    data = request.get_json(force=True)
    Flight.query.filter_by(id=id).update(
        {
        Flight._from: data["_from"],
        Flight._to: data["_to"],
        Flight.date_departure: data["date_departure"],
        Flight.date_arrival: data["date_arrival"]
        }
    )
    db.session.commit()
    flight = Flight.query.filter_by(id=id).first()
    return jsonify(
        id=flight.id,
        _from=flight._from,
        _to=flight._to,
        date_departure=flight.date_departure,
        date_arrival=flight.date_arrival)


@bp.route('/flights/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_flight(id):
    Flight.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(
        message="success"
    )


