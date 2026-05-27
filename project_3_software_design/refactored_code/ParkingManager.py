from datetime import datetime
from VehicleFactory import VehicleFactory


class ParkingLot:
    def __init__(self):
        self.capacity = 0
        self.evCapacity = 0
        self.level = 0
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        self.slots = []
        self.evSlots = []
        self._trace_observers = []

    def add_trace_observer(self, observer):
        if observer not in self._trace_observers:
            self._trace_observers.append(observer)

    def remove_trace_observer(self, observer):
        if observer in self._trace_observers:
            self._trace_observers.remove(observer)

    def _trace(self, component, message):
        for observer in self._trace_observers:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            observer(f"[{timestamp}] [{component}] {message}")

    def createParkingLot(self, capacity, evcapacity, level):
        self._trace("ParkingLot", f"createParkingLot(capacity={capacity}, evcapacity={evcapacity}, level={level})")
        
        if self.capacity > 0 or self.evCapacity > 0:
            self._trace("ParkingLot", "  → Error: Parking lot is already initialized")
            raise ValueError("Parking lot has already been initialized and cannot be recreated.")

        if capacity < 0 or evcapacity < 0 or (capacity == 0 and evcapacity == 0):
            self._trace("ParkingLot", "  → Error: Invalid capacity values")
            raise ValueError("Total capacity must be greater than 0 and cannot be negative.")

        self.capacity = capacity
        self.evCapacity = evcapacity
        self.level = level
        self.slots = [None] * capacity
        self.evSlots = [None] * evcapacity
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        self._trace("ParkingLot", f"Lot initialized: {capacity} regular slots, {evcapacity} EV slots on level {level}")
        return self.level

    def getEmptySlot(self):
        self._trace("ParkingLot", "getEmptySlot() — searching for first empty regular slot")
        try:
            idx = self.slots.index(None)
            self._trace("ParkingLot", f"  → Found empty regular slot at index {idx}")
            return idx
        except ValueError:
            self._trace("ParkingLot", "  → No empty regular slots available")
            return -1

    def getEmptyEvSlot(self):
        self._trace("ParkingLot", "getEmptyEvSlot() — searching for first empty EV slot")
        try:
            idx = self.evSlots.index(None)
            self._trace("ParkingLot", f"  → Found empty EV slot at index {idx}")
            return idx
        except ValueError:
            self._trace("ParkingLot", "  → No empty EV slots available")
            return -1

    def park(self, regnum, make, model, color, ev, motor, vehicle_type=None):
        self._trace("ParkingLot", f"park(regnum={regnum}, make={make}, model={model}, color={color}, ev={ev}, motor={motor}, vehicle_type={vehicle_type})")
        
        if not regnum or not str(regnum).strip():
            self._trace("ParkingLot", "  → Error: Missing registration number")
            raise ValueError("Registration number cannot be empty.")
            
        if self.getSlotNumFromRegNum(regnum, True) != -1 or self.getSlotNumFromRegNum(regnum, False) != -1:
            self._trace("ParkingLot", f"  → Error: Vehicle with regnum {regnum} is already parked")
            raise ValueError(f"Vehicle with registration number {regnum} is already parked.")

        if ev:
            if self.numOfOccupiedEvSlots < self.evCapacity:
                slotid = self.getEmptyEvSlot()
                if slotid != -1:
                    self._trace("ParkingLot", f"  → Delegating to VehicleFactory.create_vehicle(is_ev=True, is_motorcycle={motor}, vehicle_type={vehicle_type})")
                    self.evSlots[slotid] = VehicleFactory.create_vehicle(True, motor, regnum, make, model, color, trace=self._trace, vehicle_type=vehicle_type)
                    self.numOfOccupiedEvSlots += 1
                    self._trace("ParkingLot", f"  → Vehicle stored in EV slot index {slotid}. Allocated slot number: {slotid + 1}")
                    return slotid + 1
            self._trace("ParkingLot", "  → EV parking lot is FULL")
            return -1
        else:
            if self.numOfOccupiedSlots < self.capacity:
                slotid = self.getEmptySlot()
                if slotid != -1:
                    self._trace("ParkingLot", f"  → Delegating to VehicleFactory.create_vehicle(is_ev=False, is_motorcycle={motor}, vehicle_type={vehicle_type})")
                    self.slots[slotid] = VehicleFactory.create_vehicle(False, motor, regnum, make, model, color, trace=self._trace, vehicle_type=vehicle_type)
                    self.numOfOccupiedSlots += 1
                    self._trace("ParkingLot", f"  → Vehicle stored in regular slot index {slotid}. Allocated slot number: {slotid + 1}")
                    return slotid + 1
            self._trace("ParkingLot", "  → Regular parking lot is FULL")
            return -1

    def leave(self, slotid, ev):
        self._trace("ParkingLot", f"leave(slotid={slotid}, ev={ev})")
        index = slotid - 1
        if index < 0:
            self._trace("ParkingLot", "  → Invalid slot index (< 0)")
            return False

        if ev:
            if index < len(self.evSlots) and self.evSlots[index] is not None:
                self.evSlots[index] = None
                self.numOfOccupiedEvSlots -= 1
                self._trace("ParkingLot", f"  → EV slot {slotid} freed. Occupied EV slots: {self.numOfOccupiedEvSlots}/{self.evCapacity}")
                return True
            else:
                self._trace("ParkingLot", f"  → EV slot {slotid} is already empty or out of bounds")
        else:
            if index < len(self.slots) and self.slots[index] is not None:
                self.slots[index] = None
                self.numOfOccupiedSlots -= 1
                self._trace("ParkingLot", f"  → Regular slot {slotid} freed. Occupied regular slots: {self.numOfOccupiedSlots}/{self.capacity}")
                return True
            else:
                self._trace("ParkingLot", f"  → Regular slot {slotid} is already empty or out of bounds")
        return False

    def status(self):
        self._trace("ParkingLot", "status() — compiling lot occupancy report")
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, v in enumerate(self.slots):
            if v is not None:
                output += f"{i+1}\t{self.level}\t{v.regnum}\t\t{v.color}\t\t{v.make}\t\t{v.model}\n"

        output += "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, ev in enumerate(self.evSlots):
            if ev is not None:
                output += f"{i+1}\t{self.level}\t{ev.regnum}\t\t{ev.color}\t\t{ev.make}\t\t{ev.model}\n"
        self._trace("ParkingLot", f"  → Report generated: {self.numOfOccupiedSlots}/{self.capacity} regular, {self.numOfOccupiedEvSlots}/{self.evCapacity} EV")
        return output

    def chargeStatus(self):
        self._trace("ParkingLot", "chargeStatus() — compiling EV charge report")
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        for i, ev in enumerate(self.evSlots):
            if ev is not None:
                output += f"{i+1}\t{self.level}\t{ev.regnum}\t\t{ev.charge}\n"
        self._trace("ParkingLot", "  → EV charge report generated")
        return output

    def getRegNumFromColor(self, color, is_ev):
        self._trace("ParkingLot", f"getRegNumFromColor(color={color}, is_ev={is_ev})")
        collection = self.evSlots if is_ev else self.slots
        result = [str(v.regnum) for v in collection if v is not None and v.color == color]
        self._trace("ParkingLot", f"  → Found {len(result)} match(es)")
        return result

    def getSlotNumFromRegNum(self, regnum, is_ev):
        self._trace("ParkingLot", f"getSlotNumFromRegNum(regnum={regnum}, is_ev={is_ev})")
        collection = self.evSlots if is_ev else self.slots
        for i, v in enumerate(collection):
            if v is not None and str(v.regnum) == str(regnum):
                self._trace("ParkingLot", f"  → Found at slot number {i + 1}")
                return i + 1
        self._trace("ParkingLot", "  → Not found")
        return -1

    def getSlotNumFromColor(self, color, is_ev):
        self._trace("ParkingLot", f"getSlotNumFromColor(color={color}, is_ev={is_ev})")
        collection = self.evSlots if is_ev else self.slots
        result = [str(i + 1) for i, v in enumerate(collection) if v is not None and v.color == color]
        self._trace("ParkingLot", f"  → Found {len(result)} match(es): {result}")
        return result

    def getSlotNumFromMake(self, make, is_ev):
        self._trace("ParkingLot", f"getSlotNumFromMake(make={make}, is_ev={is_ev})")
        collection = self.evSlots if is_ev else self.slots
        result = [str(i + 1) for i, v in enumerate(collection) if v is not None and v.make == make]
        self._trace("ParkingLot", f"  → Found {len(result)} match(es): {result}")
        return result

    def getSlotNumFromModel(self, model, is_ev):
        self._trace("ParkingLot", f"getSlotNumFromModel(model={model}, is_ev={is_ev})")
        collection = self.evSlots if is_ev else self.slots
        result = [str(i + 1) for i, v in enumerate(collection) if v is not None and v.model == model]
        self._trace("ParkingLot", f"  → Found {len(result)} match(es): {result}")
        return result
