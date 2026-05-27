import unittest
from Vehicle import Bus, Car, Motorcycle, Truck
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

    def test_create_truck(self):
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

    def test_create_bus(self):
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


class TestParkingLot(unittest.TestCase):
    def setUp(self):
        self.lot = ParkingLot()

    def test_parking_lot_instances_are_independent(self):
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

    def test_trace_observers_are_instance_scoped(self):
        first_trace = []
        second_trace = []
        lot2 = ParkingLot()

        self.lot.add_trace_observer(first_trace.append)
        lot2.add_trace_observer(second_trace.append)

        self.lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        lot2.createParkingLot(capacity=1, evcapacity=0, level=2)

        self.assertTrue(first_trace)
        self.assertTrue(second_trace)
        self.assertIn("level=1", first_trace[0])
        self.assertIn("level=2", second_trace[0])

    def test_create_parking_lot(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.assertEqual(self.lot.capacity, 2)
        self.assertEqual(self.lot.evCapacity, 1)
        self.assertEqual(self.lot.level, 1)
        self.assertEqual(len(self.lot.slots), 2)
        self.assertEqual(len(self.lot.evSlots), 1)

    def test_park_vehicle_success(self):
        self.lot.createParkingLot(capacity=4, evcapacity=1, level=1)
        
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

        # Park regular truck and bus through explicit vehicle_type
        truck_slot = self.lot.park("TRK1", "Ford", "F-150", "Black", False, False, vehicle_type="truck")
        bus_slot = self.lot.park("BUS1", "Blue Bird", "Vision", "Yellow", False, False, vehicle_type="bus")
        self.assertEqual(truck_slot, 2)
        self.assertEqual(bus_slot, 3)
        self.assertIsInstance(self.lot.slots[1], Truck)
        self.assertIsInstance(self.lot.slots[2], Bus)

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

        # Test restored make/model query behavior for regular and EV slots
        honda_slots = self.lot.getSlotNumFromMake("Honda", False)
        self.assertEqual(honda_slots, ["1"])

        tesla_slots = self.lot.getSlotNumFromMake("Tesla", True)
        self.assertEqual(tesla_slots, ["1"])

        civic_slots = self.lot.getSlotNumFromModel("Civic", False)
        self.assertEqual(civic_slots, ["1"])

        model_s_slots = self.lot.getSlotNumFromModel("Model S", True)
        self.assertEqual(model_s_slots, ["1"])

if __name__ == '__main__':
    unittest.main()
