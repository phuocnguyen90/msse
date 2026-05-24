import unittest
from Vehicle import Car, Motorcycle
from ElectricVehicle import ElectricCar, ElectricBike
from VehicleFactory import VehicleFactory
from ParkingManager import ParkingLot

class TestVehicleFactory(unittest.TestCase):
    def test_create_car(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=False, regnum="123", make="Toyota", model="Corolla", color="Blue")
        self.assertIsInstance(vehicle, Car)
        self.assertEqual(vehicle.type, "Car")

    def test_create_motorcycle(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=True, regnum="456", make="Yamaha", model="R1", color="Red")
        self.assertIsInstance(vehicle, Motorcycle)
        self.assertEqual(vehicle.type, "Motorcycle")

    def test_create_electric_car(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=True, is_motorcycle=False, regnum="789", make="Tesla", model="Model 3", color="White")
        self.assertIsInstance(vehicle, ElectricCar)
        self.assertEqual(vehicle.type, "Car")

    def test_create_electric_bike(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=True, is_motorcycle=True, regnum="012", make="Zero", model="SR/F", color="Black")
        self.assertIsInstance(vehicle, ElectricBike)
        self.assertEqual(vehicle.type, "Motorcycle")


class TestParkingLot(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance for clean tests
        ParkingLot._instance = None
        self.lot = ParkingLot()

    def test_singleton(self):
        lot2 = ParkingLot()
        self.assertIs(self.lot, lot2)

    def test_create_parking_lot(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.assertEqual(self.lot.capacity, 2)
        self.assertEqual(self.lot.evCapacity, 1)
        self.assertEqual(self.lot.level, 1)
        self.assertEqual(len(self.lot.slots), 2)
        self.assertEqual(len(self.lot.evSlots), 1)

    def test_park_vehicle_success(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        
        # Park regular car
        slot1 = self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.assertEqual(slot1, 1)
        self.assertEqual(self.lot.numOfOccupiedSlots, 1)
        self.assertIsInstance(self.lot.slots[0], Car)

        # Park EV car
        ev_slot = self.lot.park("EV1", "Tesla", "Model Y", "Blue", True, False)
        self.assertEqual(ev_slot, 1)
        self.assertEqual(self.lot.numOfOccupiedEvSlots, 1)
        self.assertIsInstance(self.lot.evSlots[0], ElectricCar)

    def test_park_vehicle_full(self):
        self.lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        slot1 = self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.assertEqual(slot1, 1)
        
        # Attempt to park another regular car
        slot2 = self.lot.park("REG2", "Toyota", "Camry", "Blue", False, False)
        self.assertEqual(slot2, -1)

    def test_leave_vehicle(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        
        success = self.lot.leave(1, False)
        self.assertTrue(success)
        self.assertEqual(self.lot.numOfOccupiedSlots, 0)
        self.assertIsNone(self.lot.slots[0])

    def test_leave_invalid_slot(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success = self.lot.leave(5, False)
        self.assertFalse(success)

    def test_queries(self):
        self.lot.createParkingLot(capacity=2, evcapacity=2, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("REG2", "Toyota", "Camry", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model S", "Black", True, False)

        # Test getRegNumFromColor
        red_regs = self.lot.getRegNumFromColor("Red", False)
        self.assertEqual(red_regs, ["REG1", "REG2"])

        # Test getSlotNumFromRegNum
        ev_slot = self.lot.getSlotNumFromRegNum("EV1", True)
        self.assertEqual(ev_slot, 1)

        # Test getSlotNumFromColor
        red_slots = self.lot.getSlotNumFromColor("Red", False)
        self.assertEqual(red_slots, ["1", "2"])

if __name__ == '__main__':
    unittest.main()
