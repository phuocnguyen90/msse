"""
Unit tests for the core logic of the ParkingLot domain object.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ParkingManager import ParkingLot
from Vehicle import Car, Truck, Motorcycle, Bus
from ElectricVehicle import ElectricCar, ElectricBike
from PricingStrategy import FlatRateStrategy


class TestParkingLot(unittest.TestCase):
    """Test suite for ParkingLot initialization, parking logic, departing logic, and queries."""

    def setUp(self):
        self.lot = ParkingLot()

    def test_parking_lot_instances_are_independent(self):
        """Verify that different ParkingLot instances do not share state."""
        lot2 = ParkingLot()
        self.assertIsNot(self.lot, lot2)

        self.lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        lot2.createParkingLot(capacity=2, evcapacity=1, level=2)

        self.lot.park("FAC1", "Honda", "Civic", "Red", False, False)
        lot2.park("FAC2", "Tesla", "Model 3", "White", True, False)

        self.assertEqual(self.lot.level, 1)
        self.assertEqual(lot2.level, 2)
        self.assertEqual(self.lot.numOfOccupiedSlots, 1)
        self.assertEqual(lot2.numOfOccupiedSlots, 0)
        self.assertEqual(lot2.numOfOccupiedEvSlots, 1)

    def test_create_parking_lot(self):
        """Verify that createParkingLot initializes the lot capacity and level correctly."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.assertEqual(self.lot.capacity, 2)
        self.assertEqual(self.lot.evCapacity, 1)
        self.assertEqual(self.lot.level, 1)
        self.assertEqual(len(self.lot.slots), 2)
        self.assertEqual(len(self.lot.evSlots), 1)

    def test_create_parking_lot_negative_capacity(self):
        """Verify that attempting to create a lot with negative capacity raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.lot.createParkingLot(capacity=-1, evcapacity=1, level=1)
        self.assertIn("cannot be negative", str(context.exception))

    def test_create_parking_lot_zero_capacity(self):
        """Verify that attempting to create a lot with zero total capacity raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.lot.createParkingLot(capacity=0, evcapacity=0, level=1)
        self.assertIn("greater than 0", str(context.exception))

    def test_create_parking_lot_already_initialized(self):
        """Verify that attempting to re-initialize an already created lot raises a ValueError."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        with self.assertRaises(ValueError) as context:
            self.lot.createParkingLot(capacity=3, evcapacity=2, level=2)
        self.assertIn("already been initialized", str(context.exception))

    def test_park_regular_car(self):
        """Verify that a regular car can be parked and decreases the available regular capacity."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.assertEqual(slot, 1)
        self.assertEqual(self.lot.numOfOccupiedSlots, 1)
        self.assertIsInstance(self.lot.slots[0], Car)

    def test_park_motorcycle(self):
        """Verify that a motorcycle can be parked in the regular capacity."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("MOT1", "Yamaha", "R1", "Blue", False, True)
        self.assertEqual(slot, 1)
        self.assertIsInstance(self.lot.slots[0], Motorcycle)

    def test_park_ev_car(self):
        """Verify that an electric car can be parked and decreases the EV capacity."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("EV1", "Tesla", "Model Y", "Blue", True, False)
        self.assertEqual(slot, 1)
        self.assertEqual(self.lot.numOfOccupiedEvSlots, 1)
        self.assertIsInstance(self.lot.evSlots[0], ElectricCar)

    def test_park_truck_and_bus(self):
        """Verify that trucks and buses can be parked by specifying explicit vehicle types."""
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        truck_slot = self.lot.park("TRK1", "Ford", "F-150", "Black", False, False, vehicle_type="truck")
        bus_slot = self.lot.park("BUS1", "Blue Bird", "Vision", "Yellow", False, False, vehicle_type="bus")
        self.assertEqual(truck_slot, 1)
        self.assertEqual(bus_slot, 2)
        self.assertIsInstance(self.lot.slots[0], Truck)
        self.assertIsInstance(self.lot.slots[1], Bus)

    def test_park_ev_motorcycle(self):
        """Verify that an electric motorcycle can be parked in the EV capacity."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("EVM1", "Zero", "SR/F", "Black", True, True)
        self.assertEqual(slot, 1)
        self.assertIsInstance(self.lot.evSlots[0], ElectricBike)

    def test_park_regular_full(self):
        """Verify that attempting to park in a full regular lot returns -1."""
        self.lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        slot = self.lot.park("REG2", "Toyota", "Camry", "Blue", False, False)
        self.assertEqual(slot, -1)

    def test_park_ev_full(self):
        """Verify that attempting to park in a full EV lot returns -1."""
        self.lot.createParkingLot(capacity=1, evcapacity=1, level=1)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        slot = self.lot.park("EV2", "Tesla", "Model Y", "Red", True, False)
        self.assertEqual(slot, -1)

    def test_park_empty_regnum(self):
        """Verify that parking a vehicle without a registration number raises a ValueError."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        with self.assertRaises(ValueError) as context:
            self.lot.park("", "Honda", "Civic", "Red", False, False)
        self.assertIn("cannot be empty", str(context.exception))

    def test_park_duplicate_regnum(self):
        """Verify that parking a vehicle with a duplicate registration number raises a ValueError."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("DUP1", "Honda", "Civic", "Red", False, False)
        with self.assertRaises(ValueError) as context:
            self.lot.park("DUP1", "Toyota", "Camry", "Blue", False, False)
        self.assertIn("already parked", str(context.exception))

    def test_leave_regular(self):
        """Verify that a regular vehicle can depart, restoring capacity and calculating fees."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        success, fee = self.lot.leave(1, False)
        self.assertTrue(success)
        self.assertEqual(fee, 10.0)
        self.assertEqual(self.lot.numOfOccupiedSlots, 0)
        self.assertIsNone(self.lot.slots[0])

    def test_leave_ev(self):
        """Verify that an EV vehicle can depart, restoring EV capacity and calculating premium fees."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        success, fee = self.lot.leave(1, True)
        self.assertTrue(success)
        self.assertEqual(fee, 12.0)
        self.assertEqual(self.lot.numOfOccupiedEvSlots, 0)
        self.assertIsNone(self.lot.evSlots[0])

    def test_leave_negative_slot(self):
        """Verify that leaving an invalid negative slot index returns False."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success, fee = self.lot.leave(-1, False)
        self.assertFalse(success)

    def test_leave_out_of_bounds(self):
        """Verify that leaving an out-of-bounds slot index returns False."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success, fee = self.lot.leave(10, False)
        self.assertFalse(success)

    def test_leave_already_empty(self):
        """Verify that attempting to leave an already empty slot returns False."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success, fee = self.lot.leave(1, False)
        self.assertFalse(success)

    def test_leave_ev_already_empty(self):
        """Verify that attempting to leave an already empty EV slot returns False."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success, fee = self.lot.leave(1, True)
        self.assertFalse(success)

    def test_status_empty(self):
        """Verify that calling status() on an empty lot generates a valid report skeleton."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        status = self.lot.status()
        self.assertIn("Vehicles", status)
        self.assertIn("Electric Vehicles", status)
        self.assertNotIn("REG1", status)

    def test_status_mixed(self):
        """Verify that calling status() correctly includes mixed vehicles."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        status = self.lot.status()
        self.assertIn("REG1", status)
        self.assertIn("EV1", status)
        self.assertIn("Honda", status)
        self.assertIn("Tesla", status)

    def test_charge_status_empty(self):
        """Verify that calling chargeStatus() on an empty EV lot works without errors."""
        self.lot.createParkingLot(capacity=0, evcapacity=1, level=1)
        status = self.lot.chargeStatus()
        self.assertIn("Electric Vehicle Charge Levels", status)
        self.assertNotIn("EV1", status)

    def test_charge_status_with_values(self):
        """Verify that calling chargeStatus() correctly displays specific EV charge values."""
        self.lot.createParkingLot(capacity=0, evcapacity=2, level=1)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        self.lot.park("EV2", "Tesla", "Model Y", "Red", True, False)
        self.lot.evSlots[0].setCharge(85)
        self.lot.evSlots[1].setCharge(42)
        status = self.lot.chargeStatus()
        self.assertIn("EV1", status)
        self.assertIn("EV2", status)
        self.assertIn("85", status)
        self.assertIn("42", status)

    def test_get_reg_num_from_color(self):
        """Verify that fetching registration numbers by color returns correct lists."""
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("REG2", "Toyota", "Camry", "Red", False, False)
        self.lot.park("REG3", "Ford", "F-150", "Blue", False, False)
        red_regs = self.lot.getRegNumFromColor("Red", False)
        self.assertEqual(sorted(red_regs), ["REG1", "REG2"])

    def test_get_reg_num_from_color_not_found(self):
        """Verify that fetching registration numbers by color returns an empty list if not found."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        result = self.lot.getRegNumFromColor("Green", False)
        self.assertEqual(result, [])

    def test_get_slot_num_from_reg_num(self):
        """Verify that fetching a slot number by registration string returns the correct 1-based index."""
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        slot = self.lot.getSlotNumFromRegNum("REG1", False)
        self.assertEqual(slot, 1)
        ev_slot = self.lot.getSlotNumFromRegNum("EV1", True)
        self.assertEqual(ev_slot, 1)

    def test_get_slot_num_from_reg_num_not_found(self):
        """Verify that fetching a slot number by an unknown registration returns -1."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.getSlotNumFromRegNum("UNKNOWN", False)
        self.assertEqual(slot, -1)

    def test_get_slot_num_from_color(self):
        """Verify that fetching slot numbers by color returns correct matches."""
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("REG2", "Toyota", "Camry", "Red", False, False)
        self.lot.park("REG3", "Ford", "F-150", "Blue", False, False)
        red_slots = self.lot.getSlotNumFromColor("Red", False)
        self.assertEqual(sorted(red_slots), ["1", "2"])

    def test_get_slot_num_from_color_not_found(self):
        """Verify that fetching slot numbers by a missing color returns an empty list."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        result = self.lot.getSlotNumFromColor("Purple", False)
        self.assertEqual(result, [])

    def test_get_slot_num_from_make_and_model(self):
        """Verify that fetching slot numbers by Make and Model returns the correct string indexes."""
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model S", "White", True, False)

        honda_slots = self.lot.getSlotNumFromMake("Honda", False)
        self.assertEqual(honda_slots, ["1"])

        tesla_slots = self.lot.getSlotNumFromMake("Tesla", True)
        self.assertEqual(tesla_slots, ["1"])

        civic_slots = self.lot.getSlotNumFromModel("Civic", False)
        self.assertEqual(civic_slots, ["1"])

        model_s_slots = self.lot.getSlotNumFromModel("Model S", True)
        self.assertEqual(model_s_slots, ["1"])

    def test_lot_with_custom_strategy(self):
        """Verify that the lot properly integrates with custom PricingStrategy implementations."""
        lot = ParkingLot()
        lot.set_pricing_strategy(FlatRateStrategy(rate=42.0))
        lot.createParkingLot(capacity=2, evcapacity=0, level=1)
        lot.park("REG1", "Honda", "Civic", "Red", False, False)
        success, fee = lot.leave(1, False)
        self.assertTrue(success)
        self.assertEqual(fee, 42.0)

if __name__ == '__main__':
    unittest.main()
