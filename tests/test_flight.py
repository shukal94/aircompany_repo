import datetime
from core.controllers.flight.flights_controller import FlightsController
import pytest


class TestFlight:
    def setup(self):
        self.flights_controller = FlightsController()

    def test_admin_creates_flight(self):
        id_plane = 2
        dep = 'MINSK'
        ar = 'LONDON'
        date_from = '20-02-12 19:00'
        date_to = '21-02-15 19:00'
        self.flights_controller.create(id_plane, dep, ar, date_from, date_to)
        last_record = self.flights_controller.read()[-1]
        assert id_plane in last_record
        assert dep in last_record
        assert ar in last_record
        assert datetime.datetime.strptime(date_from, "%y-%m-%d %H:%M") in last_record
        assert datetime.datetime.strptime(date_to, "%y-%m-%d %H:%M") in last_record
