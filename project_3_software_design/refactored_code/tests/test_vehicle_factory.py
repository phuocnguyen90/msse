"""
Unit tests for the VehicleFactory class and instantiation logic.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from VehicleFactory import VehicleFactory
from Vehicle import Car, Truck, Motorcycle, Bus
from ElectricVehicle import ElectricCar, ElectricBike


class TestVehicleFactory(unittest.TestCase):
    """Test suite for validating the Factory Method pattern implementation in VehicleFactory."""

    def test_create_car(self):
        """Verify that create_vehicle correctly instantiates a regular Car."""
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=False, regnum="123", make="Toyota", model="Corolla", color="Blue")
        self.assertIsInstance(vehicle, Car)
        self.assertEqual(vehicle.type, "Car")

    def test_create_motorcycle(self):
        """Verify that create_vehicle correctly instantiates a regular Motorcycle."""
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=True, regnum="456", make="Yamaha", model="R1", color="Red")
        self.assertIsInstance(vehicle, Motorcycle)
        self.assertEqual(vehicle.type, "Motorcycle")

    def test_create_electric_car(self):
        """Verify that create_vehicle correctly instantiates an ElectricCar."""
        vehicle = VehicleFactory.create_vehicle(is_ev=True, is_motorcycle=False, regnum="789", make="Tesla", model="Model 3", color="White")
        self.assertIsInstance(vehicle, ElectricCar)
        self.assertEqual(vehicle.type, "Car")

    def test_create_electric_bike(self):
        """Verify that create_vehicle correctly instantiates an ElectricBike."""
        vehicle = VehicleFactory.create_vehicle(is_ev=True, is_motorcycle=True, regnum="012", make="Zero", model="SR/F", color="Black")
        self.assertIsInstance(vehicle, ElectricBike)
        self.assertEqual(vehicle.type, "Motorcycle")

    def test_create_truck_explicit_type(self):
        """Verify that create_vehicle instantiates a Truck when explicitly requested via vehicle_type."""
        vehicle = VehicleFactory.create_vehicle(
            is_ev=False,
            is_motorcycle=False,
            regnum="TRK1",
            make="Ford",
            model="F-150",
            color="Black",
            vehicle_type="truck",
        )
        self.assertIsInstance(vehicle, Truck)
        self.assertEqual(vehicle.type, "Truck")

    def test_create_bus_explicit_type(self):
        """Verify that create_vehicle instantiates a Bus when explicitly requested via vehicle_type."""
        vehicle = VehicleFactory.create_vehicle(
            is_ev=False,
            is_motorcycle=False,
            regnum="BUS1",
            make="Blue Bird",
            model="Vision",
            color="Yellow",
            vehicle_type="bus",
        )
        self.assertIsInstance(vehicle, Bus)
        self.assertEqual(vehicle.type, "Bus")

    def test_reject_unsupported_vehicle_type(self):
        """Verify that create_vehicle raises a ValueError for an unknown vehicle type."""
        with self.assertRaises(ValueError):
            VehicleFactory.create_vehicle(
                is_ev=False,
                is_motorcycle=False,
                regnum="VAN1",
                make="Ford",
                model="Transit",
                color="White",
                vehicle_type="van",
            )

    def test_reject_ev_truck_or_bus(self):
        """Verify that create_vehicle rejects electric trucks/buses as unsupported in this prototype."""
        with self.assertRaises(ValueError):
            VehicleFactory.create_vehicle(
                is_ev=True,
                is_motorcycle=False,
                regnum="ETRK1",
                make="Rivian",
                model="Commercial",
                color="White",
                vehicle_type="truck",
            )

if __name__ == '__main__':
    unittest.main()
