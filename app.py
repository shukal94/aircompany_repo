from flask import Flask
from core.controllers.flights.flights_controller import FlightsController
from core.controllers.users.users_controller import UsersController

flights = FlightsController()
users = UsersController()
app = Flask(__name__)

@app.route('/api/flights/', method = 'GET')
def get_all_flights():
    read_all_flights = flights.read()
    return str(read_flight)

@app.route('api/flights/<id int>', method = 'GET')
def get_flight_by_id(id):
    read_the_flight = flights.read_id(id)
    return print(read_the_flight)

@app.route('api/flights/',  method = 'DELETE')
def delete_flights():
    flights.delete_all()
    return 'all flights were deleted'

@app.route('api/flights/<id int>', method = 'DELETE')
def delete_the_flight(id):
    flights.delete_by_id(id)
    return 'flights with {0} was deleted'.format(id)

@app.route('api/flights/', method = 'POST')
def post(id_plane, _from, _to, date_departure, date_arrival):
    flights.create(id_plane, _from, _to, date_departure, date_arrival)
    return 'flight was created'

@app.route('api/flights/<id int>', method = 'PUT')
def put(_to, id_plane):
    flights.update(_to, id_plane)
    return 'flight was edited'

@app.route('api/users/', method = 'GET')
def get_all_users():
    read_all_users = users.read()
    return str(read_all_users)

@app.route('api/users/<id int>', method = 'GET')
def get_user_by_id(id):
    read_user_by_id = users.read_by_id()
    return str(read_user_by_id)

@app.route('api/users/<id int>', method = 'DELETE')
def delete_user_by_id(id):
    users.delete(id)
    return 'user was deleted'

@app.route('api/users/<id int>', method = 'POST')
def post():
    users.create(id, email, password, name, phone, address, last_name, city, state, postal_code, country, id_role)
    return 'user was posted'

@app.route('api/users/<id int>', method = 'PUT')
def put(email, phone, id):
    users.update(email, phone, id)
    return 'users was updated'




