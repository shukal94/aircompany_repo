import base64
from datetime import datetime, timedelta
import os

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from app.search import add_to_index, remove_from_index, query_index

from app import db, login


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

# MODELS


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
        default=1
    )

    token = db.Column(
        db.String(32),
        index=True,
        unique=True
    )

    token_expiration = db.Column(db.DateTime)

    flights = db.relationship(
        'Flight',
        secondary='tickets',
        backref=db.backref('tickets_ownership', lazy='dynamic'),
        lazy='dynamic'
    )

    @property
    def role(self):
        return self.query.join("roles", (self.role_id == Role.id)).first()

    @property
    def assigned_flights(self):
        raw_set = db.session.query(User, Flight).join("flights").all()
        flights = list()
        for raw_entry in raw_set:
            flights.append(raw_entry[1])
        return flights

    @property
    def assigned_tickets(self):
        raw_set = db.session.query(User, Ticket).join("flights").all()
        tickets = list()
        for raw_entry in raw_set:
            tickets.append(raw_entry[1])
        return tickets

    def buy_ticket(self, id):
        Ticket.query.filter_by(id=id).update({"user_id": current_user.id})

    def revoke_ticket(self, id):
        Ticket.query.filter_by(id=id).update({"user_id": None})

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return '<User {} {} {} {}>'.format(
            self.first_name,
            self.last_name,
            self.email,
            self.address
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
        backref='ticket_type',
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

    users = db.relationship(
        'User',
        backref='assigned_tickets'
    )

    luggages = db.relationship(
        'Luggage',
        backref='assigned_luggages'
    )

    @property
    def type(self):
        return self.query.join(TicketType).filter(
            self.type_id == TicketType.id
        ).add_columns(TicketType.name).first()[-1]

    @property
    def final_price(self):
        luggage_price = 0
        for single_luggage in self.luggages:
            luggage_price += single_luggage.price
        return self.price + luggage_price

    @property
    def assigned_luggages(self):
        return self.query.join("luggages").filter(
            self.id == Luggage.ticket_id
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
        return self.query.join(LuggageType).filter(
            self.type_id == LuggageType.id
        ).add_columns(LuggageType.name).first()[-1]

    def __repr__(self):
        return '<Luggage {}>'.format(self.price)


class Flight(SearchableMixin, db.Model):
    __tablename__ = 'flights'
    __searchable__ = ['_from', '_to']
    id = db.Column(
        db.Integer(),
        primary_key=True
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

    def __repr__(self):
        return '<Flight {} {} {} {}>'.format(self._from, self._to, self.date_departure, self.date_arrival)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
