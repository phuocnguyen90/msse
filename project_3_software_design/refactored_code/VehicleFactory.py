from Vehicle import Car, Motorcycle
from ElectricVehicle import ElectricCar, ElectricBike

class VehicleFactory:
    """
    Factory Method Pattern: Encapsulates the instantiation logic for various
    Vehicle and ElectricVehicle subtypes, removing deeply nested if-statements.
    """
    @staticmethod
    def create_vehicle(is_ev, is_motorcycle, regnum, make, model, color):
        if is_ev:
            if is_motorcycle:
                return ElectricBike(regnum, make, model, color)
            else:
                return ElectricCar(regnum, make, model, color)
        else:
            if is_motorcycle:
                return Motorcycle(regnum, make, model, color)
            else:
                return Car(regnum, make, model, color)
