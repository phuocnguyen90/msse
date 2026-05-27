"""
Unit tests for the PricingStrategy classes.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Vehicle import Car, Truck, Motorcycle, Bus
from ElectricVehicle import ElectricCar, ElectricBike
from PricingStrategy import FlatRateStrategy, EVPremiumStrategy, VehicleTypeStrategy


class TestPricingStrategy(unittest.TestCase):
    """Test suite for validating the Strategy Pattern implementation for pricing."""

    def test_flat_rate_strategy(self):
        """Verify that FlatRateStrategy returns the same configured rate for any vehicle."""
        strategy = FlatRateStrategy(rate=20.0)
        car = Car("123", "Make", "Model", "Color")
        self.assertEqual(strategy.calculate_fee(car), 20.0)

    def test_ev_premium_strategy(self):
        """Verify that EVPremiumStrategy adds a surcharge specifically for Electric Vehicles."""
        strategy = EVPremiumStrategy(base_rate=10.0, ev_surcharge=5.0)
        car = Car("123", "Make", "Model", "Color")
        ev = ElectricCar("456", "Make", "Model", "Color")
        
        self.assertEqual(strategy.calculate_fee(car), 10.0)
        self.assertEqual(strategy.calculate_fee(ev), 15.0)

    def test_vehicle_type_strategy(self):
        """Verify that VehicleTypeStrategy correctly calculates pricing based on specific subclass types."""
        strategy = VehicleTypeStrategy(motorcycle_rate=5.0, car_rate=10.0, truck_bus_rate=15.0, ev_surcharge=2.0)
        car = Car("1", "Make", "Model", "Color")
        moto = Motorcycle("2", "Make", "Model", "Color")
        truck = Truck("3", "Make", "Model", "Color")
        bus = Bus("4", "Make", "Model", "Color")
        ev_car = ElectricCar("5", "Make", "Model", "Color")
        ev_bike = ElectricBike("6", "Make", "Model", "Color")

        self.assertEqual(strategy.calculate_fee(car), 10.0)
        self.assertEqual(strategy.calculate_fee(moto), 5.0)
        self.assertEqual(strategy.calculate_fee(truck), 15.0)
        self.assertEqual(strategy.calculate_fee(bus), 15.0)
        self.assertEqual(strategy.calculate_fee(ev_car), 12.0)
        self.assertEqual(strategy.calculate_fee(ev_bike), 7.0)

if __name__ == '__main__':
    unittest.main()
