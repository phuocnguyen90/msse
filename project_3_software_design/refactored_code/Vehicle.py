# Vehicle class hierarchy for Parking Lot Manager
class Vehicle:
    def __init__(self, regnum, make, model, color):
        self.color = color
        self.regnum = regnum
        self.make = make
        self.model = model

    @property
    def type(self):
        return self.__class__.__name__


class Car(Vehicle):
    pass


class Truck(Vehicle):
    pass


class Motorcycle(Vehicle):
    pass


class Bus(Vehicle):
    pass
