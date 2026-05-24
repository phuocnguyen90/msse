from Vehicle import Vehicle

class ElectricVehicle(Vehicle):
    def __init__(self, regnum, make, model, color):
        super().__init__(regnum, make, model, color)
        self.charge = 0

    def setCharge(self, charge):
        self.charge = charge

    def getCharge(self):
        return self.charge


class ElectricCar(ElectricVehicle):
    @property
    def type(self):
        return "Car"


class ElectricBike(ElectricVehicle):
    @property
    def type(self):
        return "Motorcycle"
