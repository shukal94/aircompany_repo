from collections import namedtuple
from datetime import datetime
from functools import reduce

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        unique=True
    )
    users = db.relationship(
        'User',
        backref='role',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(50),
        index=True,
        unique=True
    )
    first_name = db.Column(
        db.String(64),
        nullable=False
    )
    last_name = db.Column(
        db.String(64),
        nullable=False
    )
    email = db.Column(
        db.String(120),
        index=True,
        unique=True
    )
    password_hash = db.Column(
        db.String(128),
        default=None
    )
    address = db.Column(
        db.String(64),
        nullable=False
    )
    country = db.Column(
        db.String(64),
        default=None
    )
    state = db.Column(
        db.String(64),
        default=None
    )
    postal_code = db.Column(
        db.Integer,
        nullable=False
    )
    about_me = db.Column(db.String(140))
    last_seen = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    role_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'roles.id',
            ondelete='CASCADE'
        ),
        default=None
    )
    tickets = db.relationship(
        'Ticket',
        backref='user_tickets',
        lazy='dynamic'
    )
    flights = db.relationship(
        'Flight',
        secondary='tickets',
        backref='owner',
        lazy='dynamic'
    )

    @property
    def role(self):
        return User.query.join("roles").first()

    @property
    def user_flights(self):
        return User.query.join("tickets").join("flights")\
            .filter(
                self.id == Ticket.user_id,
                Ticket.flight_id == Flight.id
                )\
                .add_column(Ticket.price).filter(Ticket.user_id == self.id)\
                .add_columns(
                    Flight.date_departure,
                    Flight.date_arrival,
                    Flight._from,
                    Flight._to
            )\
        .filter(Ticket.flight_id == Flight.id).all()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return '<User {} {} {} {}>'.format(
            self.first_name,
            self.last_name,
            self.email,
            self.address
        )


class Plane(db.Model):
    __tablename__ = 'planes'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    manufacturer = db.Column(
        db.String(50),
        nullable=False
    )
    model = db.Column(
        db.String(50),
        nullable=False
    )
    biz_seats_num = db.Column(
        db.Integer(),
        nullable=False
    )
    econom_seats_num = db.Column(
        db.Integer(),
        nullable=False
    )
    vip_seats_num = db.Column(
        db.Integer(),
        nullable=False
    )
    flights = db.relationship(
        'Flight',
        backref='transport',
        lazy='dynamic'
    )

    @property
    def capacity(self):
        return self.vip_seats_num + self.econom_seats_num + self.biz_seats_num

    def __repr__(self):
        return '<Plane {} {} {}>'.format(
            self.manufacturer,
            self.model,
            self.capacity
        )


class TicketType(db.Model):
    __tablename__ = 'ticket_types'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        unique=True
    )
    tickets = db.relationship(
        'Ticket',
        backref='type_of_ticket',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<TicketType {}>'.format(self.name)


class LuggageType(db.Model):
    __tablename__ = 'luggage_types'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        unique=True
    )
    luggages = db.relationship(
        'Luggage',
        backref='type_of_luggage',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<luggageType {}>'.format(self.name)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    flight_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'flights.id',
            ondelete='CASCADE'
        )
    )
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'users.id',
            ondelete='CASCADE'
        )
    )
    type_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'ticket_types.id',
            ondelete='CASCADE'
        )
    )
    price = db.Column(
        db.Float(
            asdecimal=True
        ),
        nullable=False
    )
    ticket_luggages = db.relationship(
        'Luggage',
        backref='load',
        lazy='dynamic'
    )

    @property
    def type(self):
        return Ticket.query.join("ticket_types").first()

    @property
    def final_price(self):
        luggage_price = 0
        ticket_luggages = namedtuple(
            'Luggages', [
                'Ticket',
                'price',
                'name'
            ]
        )
        for luggage in map(ticket_luggages._make, self.luggages):
            luggage_price += luggage.price
        return self.price + luggage_price


    @property
    def luggages(self):
        return Ticket.query.join("luggages").filter(
            self.id == Luggage.ticket_id
        ).add_columns(
            Luggage.price,
            Luggage.type.name
        ).all()

    def __repr__(self):
        return '<Ticket {}>'.format(self.price)


class Luggage(db.Model):
    __tablename__ = 'luggages'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    type_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'luggage_types.id',
            ondelete='CASCADE'
        )
    )
    ticket_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'tickets.id',
            ondelete='CASCADE'
        )
    )
    price = db.Column(
        db.Float(
            asdecimal=True
        ),
        nullable=False
    )

    @property
    def type(self):
        return Luggage.query.join("luggage_types").first()

    def __repr__(self):
        return '<Luggage {}>'.format(self.price)


class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    plane_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'planes.id',
            ondelete='CASCADE'
        )
    )
    _from = db.Column(
        db.String(50),
        nullable=False
    )
    _to = db.Column(
        db.String(50),
        nullable=False
    )
    date_departure = db.Column(
        db.DateTime,
        nullable=False
    )
    date_arrival = db.Column(
        db.DateTime,
        nullable=False
    )
    tickets = db.relationship(
        'Ticket',
        backref='container',
        lazy='dynamic'
    )

    @property
    def plane(self):
        return Flight.query.join("planes").first()

    def __repr__(self):
        return '<Flight {} {} {} {}>'.format(self._from, self._to, self.date_departure, self.date_arrival)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
