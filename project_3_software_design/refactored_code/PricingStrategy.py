from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Abstract base class for all pricing strategies."""
    
    @abstractmethod
    def calculate_fee(self, vehicle):
        """Calculate the parking fee for the given vehicle."""
        pass

class FlatRateStrategy(PricingStrategy):
    """A strategy that charges a fixed flat rate for all vehicles."""
    
    def __init__(self, rate=10.0):
        self.rate = rate

    def calculate_fee(self, vehicle):
        return self.rate

class EVPremiumStrategy(PricingStrategy):
    """A strategy that charges a base rate, plus a surcharge for electric vehicles."""
    
    def __init__(self, base_rate=10.0, ev_surcharge=5.0):
        self.base_rate = base_rate
        self.ev_surcharge = ev_surcharge

    def calculate_fee(self, vehicle):
        fee = self.base_rate
        # Check if it's an electric vehicle (they have a 'charge' attribute)
        if hasattr(vehicle, 'charge'):
            fee += self.ev_surcharge
        return fee

class VehicleTypeStrategy(PricingStrategy):
    """A strategy that charges different rates based on the vehicle type."""
    
    def __init__(self, motorcycle_rate=5.0, car_rate=10.0, truck_bus_rate=15.0, ev_surcharge=2.0):
        self.motorcycle_rate = motorcycle_rate
        self.car_rate = car_rate
        self.truck_bus_rate = truck_bus_rate
        self.ev_surcharge = ev_surcharge

    def calculate_fee(self, vehicle):
        fee = self.car_rate  # Default fallback
        vtype = vehicle.type.lower() if hasattr(vehicle, 'type') else "car"
        
        if vtype == 'motorcycle':
            fee = self.motorcycle_rate
        elif vtype == 'car':
            fee = self.car_rate
        elif vtype in ('truck', 'bus'):
            fee = self.truck_bus_rate

        if hasattr(vehicle, 'charge'):
            fee += self.ev_surcharge

        return fee
