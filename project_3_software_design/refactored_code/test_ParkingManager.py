import unittest
from Vehicle import Vehicle, Car, Truck, Motorcycle, Bus
from ElectricVehicle import ElectricVehicle, ElectricCar, ElectricBike
from VehicleFactory import VehicleFactory
from ParkingManager import ParkingLot


class TestVehicleFactory(unittest.TestCase):
    def test_create_car(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=False, regnum="123", make="Toyota", model="Corolla", color="Blue")
        self.assertIsInstance(vehicle, Car)
        self.assertEqual(vehicle.type, "Car")

    def test_create_truck(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=False, regnum="T01", make="Ford", model="F-150", color="Black")
        self.assertIsInstance(vehicle, Car)
        self.assertEqual(vehicle.type, "Car")

    def test_create_motorcycle(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=True, regnum="456", make="Yamaha", model="R1", color="Red")
        self.assertIsInstance(vehicle, Motorcycle)
        self.assertEqual(vehicle.type, "Motorcycle")

    def test_create_bus(self):
        vehicle = VehicleFactory.create_vehicle(is_ev=False, is_motorcycle=False, regnum="B01", make="Volvo", model="7900", color="Yellow")
        self.assertIsInstance(vehicle, Car)
        self.assertEqual(vehicle.type, "Car")

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


class TestVehicleProperties(unittest.TestCase):
    def test_base_vehicle_attributes(self):
        v = Vehicle("ABC123", "Honda", "Civic", "Red")
        self.assertEqual(v.regnum, "ABC123")
        self.assertEqual(v.make, "Honda")
        self.assertEqual(v.model, "Civic")
        self.assertEqual(v.color, "Red")
        self.assertEqual(v.type, "Vehicle")

    def test_car_inheritance(self):
        c = Car("DEF456", "Toyota", "Camry", "Blue")
        self.assertIsInstance(c, Vehicle)
        self.assertEqual(c.type, "Car")

    def test_truck_inheritance(self):
        t = Truck("TRK01", "Ford", "F-150", "Black")
        self.assertIsInstance(t, Vehicle)
        self.assertEqual(t.type, "Truck")

    def test_motorcycle_inheritance(self):
        m = Motorcycle("MOT01", "Yamaha", "R1", "Green")
        self.assertIsInstance(m, Vehicle)
        self.assertEqual(m.type, "Motorcycle")

    def test_bus_inheritance(self):
        b = Bus("BUS01", "Volvo", "7900", "Yellow")
        self.assertIsInstance(b, Vehicle)
        self.assertEqual(b.type, "Bus")

    def test_electric_vehicle_charge(self):
        ev = ElectricVehicle("EV01", "Tesla", "Model S", "White")
        self.assertEqual(ev.getCharge(), 0)
        ev.setCharge(85)
        self.assertEqual(ev.getCharge(), 85)

    def test_electric_car_inheritance(self):
        ec = ElectricCar("EV02", "Tesla", "Model 3", "Red")
        self.assertIsInstance(ec, ElectricVehicle)
        self.assertIsInstance(ec, Vehicle)
        self.assertEqual(ec.type, "Car")

    def test_electric_bike_inheritance(self):
        eb = ElectricBike("EV03", "Zero", "SR/F", "Black")
        self.assertIsInstance(eb, ElectricVehicle)
        self.assertIsInstance(eb, Vehicle)
        self.assertEqual(eb.type, "Motorcycle")


class TestParkingLot(unittest.TestCase):
    def setUp(self):
        ParkingLot._instance = None
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

    def test_create_parking_lot_negative_capacity(self):
        with self.assertRaises(ValueError) as context:
            self.lot.createParkingLot(capacity=-1, evcapacity=1, level=1)
        self.assertIn("cannot be negative", str(context.exception))

    def test_create_parking_lot_zero_capacity(self):
        with self.assertRaises(ValueError) as context:
            self.lot.createParkingLot(capacity=0, evcapacity=0, level=1)
        self.assertIn("greater than 0", str(context.exception))

    def test_create_parking_lot_already_initialized(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        with self.assertRaises(ValueError) as context:
            self.lot.createParkingLot(capacity=3, evcapacity=2, level=2)
        self.assertIn("already been initialized", str(context.exception))

    def test_park_regular_car(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.assertEqual(slot, 1)
        self.assertEqual(self.lot.numOfOccupiedSlots, 1)
        self.assertIsInstance(self.lot.slots[0], Car)

    def test_park_motorcycle(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("MOT1", "Yamaha", "R1", "Blue", False, True)
        self.assertEqual(slot, 1)
        self.assertIsInstance(self.lot.slots[0], Motorcycle)

    def test_park_ev_car(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("EV1", "Tesla", "Model Y", "Blue", True, False)
        self.assertEqual(slot, 1)
        self.assertEqual(self.lot.numOfOccupiedEvSlots, 1)
        self.assertIsInstance(self.lot.evSlots[0], ElectricCar)

    def test_park_truck_and_bus(self):
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        # Park regular truck and bus through explicit vehicle_type
        truck_slot = self.lot.park("TRK1", "Ford", "F-150", "Black", False, False, vehicle_type="truck")
        bus_slot = self.lot.park("BUS1", "Blue Bird", "Vision", "Yellow", False, False, vehicle_type="bus")
        self.assertEqual(truck_slot, 1)
        self.assertEqual(bus_slot, 2)
        self.assertIsInstance(self.lot.slots[0], Truck)
        self.assertIsInstance(self.lot.slots[1], Bus)

    def test_park_ev_motorcycle(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.park("EVM1", "Zero", "SR/F", "Black", True, True)
        self.assertEqual(slot, 1)
        self.assertIsInstance(self.lot.evSlots[0], ElectricBike)

    def test_park_regular_full(self):
        self.lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        slot = self.lot.park("REG2", "Toyota", "Camry", "Blue", False, False)
        self.assertEqual(slot, -1)

    def test_park_ev_full(self):
        self.lot.createParkingLot(capacity=1, evcapacity=1, level=1)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        slot = self.lot.park("EV2", "Tesla", "Model Y", "Red", True, False)
        self.assertEqual(slot, -1)

    def test_park_empty_regnum(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        with self.assertRaises(ValueError) as context:
            self.lot.park("", "Honda", "Civic", "Red", False, False)
        self.assertIn("cannot be empty", str(context.exception))

    def test_park_duplicate_regnum(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("DUP1", "Honda", "Civic", "Red", False, False)
        with self.assertRaises(ValueError) as context:
            self.lot.park("DUP1", "Toyota", "Camry", "Blue", False, False)
        self.assertIn("already parked", str(context.exception))

    def test_leave_regular(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        success = self.lot.leave(1, False)
        self.assertTrue(success)
        self.assertEqual(self.lot.numOfOccupiedSlots, 0)
        self.assertIsNone(self.lot.slots[0])

    def test_leave_ev(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        success = self.lot.leave(1, True)
        self.assertTrue(success)
        self.assertEqual(self.lot.numOfOccupiedEvSlots, 0)
        self.assertIsNone(self.lot.evSlots[0])

    def test_leave_negative_slot(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success = self.lot.leave(-1, False)
        self.assertFalse(success)

    def test_leave_out_of_bounds(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success = self.lot.leave(10, False)
        self.assertFalse(success)

    def test_leave_already_empty(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success = self.lot.leave(1, False)
        self.assertFalse(success)

    def test_leave_ev_already_empty(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        success = self.lot.leave(1, True)
        self.assertFalse(success)

    def test_status_empty(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        status = self.lot.status()
        self.assertIn("Vehicles", status)
        self.assertIn("Electric Vehicles", status)
        self.assertNotIn("REG1", status)

    def test_status_mixed(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        status = self.lot.status()
        self.assertIn("REG1", status)
        self.assertIn("EV1", status)
        self.assertIn("Honda", status)
        self.assertIn("Tesla", status)

    def test_charge_status_empty(self):
        self.lot.createParkingLot(capacity=0, evcapacity=1, level=1)
        status = self.lot.chargeStatus()
        self.assertIn("Electric Vehicle Charge Levels", status)
        self.assertNotIn("EV1", status)

    def test_charge_status_with_values(self):
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
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("REG2", "Toyota", "Camry", "Red", False, False)
        self.lot.park("REG3", "Ford", "F-150", "Blue", False, False)
        red_regs = self.lot.getRegNumFromColor("Red", False)
        self.assertEqual(sorted(red_regs), ["REG1", "REG2"])

    def test_get_reg_num_from_color_not_found(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        result = self.lot.getRegNumFromColor("Green", False)
        self.assertEqual(result, [])

    def test_get_slot_num_from_reg_num(self):
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model 3", "White", True, False)
        slot = self.lot.getSlotNumFromRegNum("REG1", False)
        self.assertEqual(slot, 1)
        ev_slot = self.lot.getSlotNumFromRegNum("EV1", True)
        self.assertEqual(ev_slot, 1)

    def test_get_slot_num_from_reg_num_not_found(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        slot = self.lot.getSlotNumFromRegNum("UNKNOWN", False)
        self.assertEqual(slot, -1)

    def test_get_slot_num_from_color(self):
        self.lot.createParkingLot(capacity=3, evcapacity=1, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.park("REG2", "Toyota", "Camry", "Red", False, False)
        self.lot.park("REG3", "Ford", "F-150", "Blue", False, False)
        red_slots = self.lot.getSlotNumFromColor("Red", False)
        self.assertEqual(sorted(red_slots), ["1", "2"])

    def test_get_slot_num_from_color_not_found(self):
        self.lot.createParkingLot(capacity=2, evcapacity=1, level=1)
        result = self.lot.getSlotNumFromColor("Purple", False)
        self.assertEqual(result, [])

    def test_tracing_create_and_park(self):
        traced_messages = []
        def mock_trace(message):
            traced_messages.append(message)

        ParkingLot.set_trace_callback(mock_trace)
        ParkingLot._instance = None
        lot = ParkingLot()
        lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        lot.park("REG1", "Honda", "Civic", "Red", False, False)

        self.assertGreater(len(traced_messages), 0)
        self.assertTrue(any("createParkingLot" in msg for msg in traced_messages))
        self.assertTrue(any("park" in msg for msg in traced_messages))
        self.assertTrue(any("Singleton" in msg for msg in traced_messages))

        ParkingLot.set_trace_callback(None)

    def test_tracing_leave(self):
        traced_messages = []
        def mock_trace(message):
            traced_messages.append(message)

        ParkingLot.set_trace_callback(mock_trace)
        self.lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        self.lot.park("REG1", "Honda", "Civic", "Red", False, False)
        self.lot.leave(1, False)

        self.assertTrue(any("leave" in msg for msg in traced_messages))

        ParkingLot.set_trace_callback(None)


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
