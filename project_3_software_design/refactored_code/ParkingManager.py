from datetime import datetime
from VehicleFactory import VehicleFactory
from PricingStrategy import VehicleTypeStrategy
from DomainEvents import (
    LotInitializedEvent,
    VehicleParkedEvent,
    VehicleDepartedEvent,
    VehicleParkFailedEvent,
    VehicleDepartFailedEvent,
    PricingStrategyChangedEvent
)

class ParkingLot:
    def __init__(self, pricing_strategy=None):
        self.capacity = 0
        self.evCapacity = 0
        self.level = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        self.slots = []
        self.evSlots = []
        self.event_observers = []
        self.pricing_strategy = pricing_strategy if pricing_strategy else VehicleTypeStrategy()

    def add_event_observer(self, observer):
        if observer not in self.event_observers:
            self.event_observers.append(observer)

    def remove_event_observer(self, observer):
        if observer in self.event_observers:
            self.event_observers.remove(observer)

    def publish(self, event):
        for observer in self.event_observers:
            observer(event)

    def set_pricing_strategy(self, strategy):
        self.pricing_strategy = strategy
        self.publish(PricingStrategyChangedEvent(strategy.__class__.__name__))

    def createParkingLot(self, capacity, evcapacity, level):
        if self.capacity > 0 or self.evCapacity > 0:
            raise ValueError("Parking lot has already been initialized and cannot be recreated.")

        if capacity < 0 or evcapacity < 0 or (capacity == 0 and evcapacity == 0):
            raise ValueError("Total capacity must be greater than 0 and cannot be negative.")

        self.capacity = capacity
        self.evCapacity = evcapacity
        self.level = level
        self.slots = [None] * capacity
        self.evSlots = [None] * evcapacity
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        self.publish(LotInitializedEvent(capacity, evcapacity, level))
        return self.level

    def getEmptySlot(self):
        try:
            return self.slots.index(None)
        except ValueError:
            return -1

    def getEmptyEvSlot(self):
        try:
            return self.evSlots.index(None)
        except ValueError:
            return -1

    def park(self, regnum, make, model, color, ev, motor, vehicle_type=None):
        if not regnum or not str(regnum).strip():
            self.publish(VehicleParkFailedEvent("Missing registration number"))
            raise ValueError("Registration number cannot be empty.")
            
        if self.getSlotNumFromRegNum(regnum, True) != -1 or self.getSlotNumFromRegNum(regnum, False) != -1:
            self.publish(VehicleParkFailedEvent(f"Vehicle with regnum {regnum} is already parked"))
            raise ValueError(f"Vehicle with registration number {regnum} is already parked.")

        if ev:
            if self.numOfOccupiedEvSlots < self.evCapacity:
                slotid = self.getEmptyEvSlot()
                if slotid != -1:
                    vehicle = VehicleFactory.create_vehicle(True, motor, regnum, make, model, color, vehicle_type=vehicle_type)
                    self.evSlots[slotid] = vehicle
                    self.numOfOccupiedEvSlots += 1
                    self.publish(VehicleParkedEvent(vehicle, slotid + 1, True))
                    return slotid + 1
            self.publish(VehicleParkFailedEvent("EV parking lot is FULL"))
            return -1
        else:
            if self.numOfOccupiedSlots < self.capacity:
                slotid = self.getEmptySlot()
                if slotid != -1:
                    vehicle = VehicleFactory.create_vehicle(False, motor, regnum, make, model, color, vehicle_type=vehicle_type)
                    self.slots[slotid] = vehicle
                    self.numOfOccupiedSlots += 1
                    self.publish(VehicleParkedEvent(vehicle, slotid + 1, False))
                    return slotid + 1
            self.publish(VehicleParkFailedEvent("Regular parking lot is FULL"))
            return -1

    def leave(self, slotid, ev):
        index = slotid - 1
        if index < 0:
            self.publish(VehicleDepartFailedEvent("Invalid slot index (< 0)"))
            return False, 0.0

        if ev:
            if index < len(self.evSlots) and self.evSlots[index] is not None:
                vehicle = self.evSlots[index]
                fee = self.pricing_strategy.calculate_fee(vehicle)
                self.evSlots[index] = None
                self.numOfOccupiedEvSlots -= 1
                self.publish(VehicleDepartedEvent(vehicle, slotid, True, fee))
                return True, fee
            else:
                self.publish(VehicleDepartFailedEvent(f"EV slot {slotid} is already empty or out of bounds"))
        else:
            if index < len(self.slots) and self.slots[index] is not None:
                vehicle = self.slots[index]
                fee = self.pricing_strategy.calculate_fee(vehicle)
                self.slots[index] = None
                self.numOfOccupiedSlots -= 1
                self.publish(VehicleDepartedEvent(vehicle, slotid, False, fee))
                return True, fee
            else:
                self.publish(VehicleDepartFailedEvent(f"Regular slot {slotid} is already empty or out of bounds"))
        return False, 0.0

    def status(self):
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, v in enumerate(self.slots):
            if v is not None:
                output += f"{i+1}\t{self.level}\t{v.regnum}\t\t{v.color}\t\t{v.make}\t\t{v.model}\n"

        output += "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, ev in enumerate(self.evSlots):
            if ev is not None:
                output += f"{i+1}\t{self.level}\t{ev.regnum}\t\t{ev.color}\t\t{ev.make}\t\t{ev.model}\n"
        return output

    def chargeStatus(self):
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        for i, ev in enumerate(self.evSlots):
            if ev is not None:
                output += f"{i+1}\t{self.level}\t{ev.regnum}\t\t{ev.charge}\n"
        return output

    def getRegNumFromColor(self, color, is_ev):
        collection = self.evSlots if is_ev else self.slots
        return [str(v.regnum) for v in collection if v is not None and v.color == color]

    def getSlotNumFromRegNum(self, regnum, is_ev):
        collection = self.evSlots if is_ev else self.slots
        for i, v in enumerate(collection):
            if v is not None and str(v.regnum) == str(regnum):
                return i + 1
        return -1

    def getSlotNumFromColor(self, color, is_ev):
        collection = self.evSlots if is_ev else self.slots
        return [str(i + 1) for i, v in enumerate(collection) if v is not None and v.color == color]

    def getSlotNumFromMake(self, make, is_ev):
        collection = self.evSlots if is_ev else self.slots
        return [str(i + 1) for i, v in enumerate(collection) if v is not None and v.make == make]

    def getSlotNumFromModel(self, model, is_ev):
        collection = self.evSlots if is_ev else self.slots
        return [str(i + 1) for i, v in enumerate(collection) if v is not None and v.model == model]
