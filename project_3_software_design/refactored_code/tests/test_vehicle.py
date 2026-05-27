"""
Unit tests for vehicle property initialization and inheritance.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Vehicle import Vehicle, Car, Truck, Motorcycle, Bus
from ElectricVehicle import ElectricVehicle, ElectricCar, ElectricBike


class TestVehicleProperties(unittest.TestCase):
    """Test suite for Vehicle attributes and inheritance hierarchies."""

    def test_base_vehicle_attributes(self):
        """Verify that the base Vehicle class correctly assigns registration, make, model, color, and type."""
        v = Vehicle("ABC123", "Honda", "Civic", "Red")
        self.assertEqual(v.regnum, "ABC123")
        self.assertEqual(v.make, "Honda")
        self.assertEqual(v.model, "Civic")
        self.assertEqual(v.color, "Red")
        self.assertEqual(v.type, "Vehicle")

    def test_car_inheritance(self):
        """Verify that Car inherits from Vehicle and has the correct type."""
        c = Car("DEF456", "Toyota", "Camry", "Blue")
        self.assertIsInstance(c, Vehicle)
        self.assertEqual(c.type, "Car")

    def test_truck_inheritance(self):
        """Verify that Truck inherits from Vehicle and has the correct type."""
        t = Truck("TRK01", "Ford", "F-150", "Black")
        self.assertIsInstance(t, Vehicle)
        self.assertEqual(t.type, "Truck")

    def test_motorcycle_inheritance(self):
        """Verify that Motorcycle inherits from Vehicle and has the correct type."""
        m = Motorcycle("MOT01", "Yamaha", "R1", "Green")
        self.assertIsInstance(m, Vehicle)
        self.assertEqual(m.type, "Motorcycle")

    def test_bus_inheritance(self):
        """Verify that Bus inherits from Vehicle and has the correct type."""
        b = Bus("BUS01", "Volvo", "7900", "Yellow")
        self.assertIsInstance(b, Vehicle)
        self.assertEqual(b.type, "Bus")

    def test_electric_vehicle_charge(self):
        """Verify that ElectricVehicle charge starts at 0 and can be updated."""
        ev = ElectricVehicle("EV01", "Tesla", "Model S", "White")
        self.assertEqual(ev.getCharge(), 0)
        ev.setCharge(85)
        self.assertEqual(ev.getCharge(), 85)

    def test_electric_car_inheritance(self):
        """Verify that ElectricCar inherits from both ElectricVehicle and Vehicle."""
        ec = ElectricCar("EV02", "Tesla", "Model 3", "Red")
        self.assertIsInstance(ec, ElectricVehicle)
        self.assertIsInstance(ec, Vehicle)
        self.assertEqual(ec.type, "Car")

    def test_electric_bike_inheritance(self):
        """Verify that ElectricBike inherits from both ElectricVehicle and Vehicle, acting as a motorcycle."""
        eb = ElectricBike("EV03", "Zero", "SR/F", "Black")
        self.assertIsInstance(eb, ElectricVehicle)
        self.assertIsInstance(eb, Vehicle)
        self.assertEqual(eb.type, "Motorcycle")

if __name__ == '__main__':
    unittest.main()
