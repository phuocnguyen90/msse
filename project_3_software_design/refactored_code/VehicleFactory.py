from Vehicle import Bus, Car, Motorcycle, Truck
from ElectricVehicle import ElectricCar, ElectricBike


class VehicleFactory:
    @staticmethod
    def create_vehicle(is_ev, is_motorcycle, regnum, make, model, color, vehicle_type=None):
        normalized_type = vehicle_type.lower() if vehicle_type else None

        if normalized_type in ("truck", "bus") and is_ev:
            raise ValueError("Truck and bus are only supported as regular vehicles in this prototype.")

        vehicle_classes = {
            "car": Car,
            "motorcycle": Motorcycle,
            "truck": Truck,
            "bus": Bus,
            "electric_car": ElectricCar,
            "electric_bike": ElectricBike,
            "electric_motorcycle": ElectricBike,
        }

        if normalized_type:
            if normalized_type not in vehicle_classes:
                raise ValueError(f"Unsupported vehicle type: {vehicle_type}")
            vehicle_class = vehicle_classes[normalized_type]
        elif is_ev:
            vehicle_class = ElectricBike if is_motorcycle else ElectricCar
        else:
            vehicle_class = Motorcycle if is_motorcycle else Car

        vehicle = vehicle_class(regnum, make, model, color)

        return vehicle
