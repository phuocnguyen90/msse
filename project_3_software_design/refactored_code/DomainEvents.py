from datetime import datetime

class DomainEvent:
    def __init__(self):
        self.timestamp = datetime.now()

class LotInitializedEvent(DomainEvent):
    def __init__(self, capacity, ev_capacity, level):
        super().__init__()
        self.capacity = capacity
        self.ev_capacity = ev_capacity
        self.level = level

    def __str__(self):
        return f"Lot initialized: {self.capacity} regular slots, {self.ev_capacity} EV slots on level {self.level}"

class VehicleParkedEvent(DomainEvent):
    def __init__(self, vehicle, slot_id, is_ev):
        super().__init__()
        self.vehicle = vehicle
        self.slot_id = slot_id
        self.is_ev = is_ev

    def __str__(self):
        slot_type = "EV" if self.is_ev else "Regular"
        return f"Vehicle stored in {slot_type} slot index {self.slot_id - 1}. Allocated slot number: {self.slot_id}"

class VehicleDepartedEvent(DomainEvent):
    def __init__(self, vehicle, slot_id, is_ev, fee):
        super().__init__()
        self.vehicle = vehicle
        self.slot_id = slot_id
        self.is_ev = is_ev
        self.fee = fee

    def __str__(self):
        slot_type = "EV" if self.is_ev else "Regular"
        return f"{slot_type} slot {self.slot_id} freed. Parking fee: ${self.fee:.2f}"

class VehicleParkFailedEvent(DomainEvent):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def __str__(self):
        return f"Failed to park: {self.reason}"

class VehicleDepartFailedEvent(DomainEvent):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def __str__(self):
        return f"Failed to depart: {self.reason}"

class PricingStrategyChangedEvent(DomainEvent):
    def __init__(self, strategy_name):
        super().__init__()
        self.strategy_name = strategy_name

    def __str__(self):
        return f"Pricing strategy changed to: {self.strategy_name}"
