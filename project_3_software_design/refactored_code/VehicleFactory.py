from Vehicle import Car, Motorcycle
from ElectricVehicle import ElectricCar, ElectricBike


class VehicleFactory:
    @staticmethod
    def create_vehicle(is_ev, is_motorcycle, regnum, make, model, color, trace=None):
        vehicle_type = "Unknown"
        if is_ev:
            if is_motorcycle:
                vehicle_type = "ElectricBike"
                vehicle = ElectricBike(regnum, make, model, color)
            else:
                vehicle_type = "ElectricCar"
                vehicle = ElectricCar(regnum, make, model, color)
        else:
            if is_motorcycle:
                vehicle_type = "Motorcycle"
                vehicle = Motorcycle(regnum, make, model, color)
            else:
                vehicle_type = "Car"
                vehicle = Car(regnum, make, model, color)

        if trace:
            trace("VehicleFactory", f"  → Created {vehicle_type}(regnum={regnum}, make={make}, model={model}, color={color})")
        return vehicle
