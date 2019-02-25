from core.controllers.flights.flights_controller import FlightsController


flights_controller = FlightsController()
# flights_controller.create(3,"'MINSK'","'LONDON'","'20-02-12 19:00'", "'21-02-15 19:00'")
# # flights_controller.update("'GOMEL'",0)
# flights_controller.delete(3)
print(flights_controller.read())