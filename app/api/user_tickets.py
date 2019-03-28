from app.api import bp
from app.models import User

from flask import jsonify
from app.api.auth import token_auth


@bp.route('/users/<int:user_id>/tickets')
@token_auth.login_required
def get_user_tickets(user_id):
    user_tickets = User.query.filter_by(id=user_id).first().assigned_tickets
    user_tickets_for_json = [
        {
            "flight_id": ticket.flight_id,
            "type": ticket.type
        } for ticket in user_tickets
    ]
    return jsonify(user_tickets_for_json)
