# UML Diagrams (Original vs. Refactored)

As required by the project rubrics, here are the two sets of UML diagrams (Structural and Behavioral) representing the application before and after refactoring.

---

## Part 1: Original Codebase

### 1. Structural Diagram (Class Diagram)
This diagram illustrates the original, tightly coupled structure. Notice the broken inheritance chain where `ElectricCar` and `ElectricBike` fail to properly extend `ElectricVehicle`. The `ParkingLot` directly instantiates multiple concrete classes, creating tight coupling.

```mermaid
classDiagram
    class ParkingLot {
        +int capacity
        +int evCapacity
        +int level
        +list slots
        +list evSlots
        +createParkingLot(capacity, evcapacity, level)
        +park(regnum, make, model, color, ev, motor)
        +leave(slotid, ev)
        +edit(slotid, regnum, make, model, color, ev)
        +status()
    }
    
    class Vehicle {
        +string regnum
        +string make
        +string model
        +string color
        +getMake()
        +getModel()
        +getColor()
        +getRegNum()
    }
    class Car {
        +getType()
    }
    class Truck {
        +getType()
    }
    class Motorcycle {
        +getType()
    }
    class Bus {
        +getType()
    }
    Vehicle <|-- Car
    Vehicle <|-- Truck
    Vehicle <|-- Motorcycle
    Vehicle <|-- Bus
    
    class ElectricVehicle {
        +string regnum
        +string make
        +string model
        +string color
        +int charge
        +getCharge()
        +setCharge(charge)
    }
    class ElectricCar {
        +getType()
    }
    class ElectricBike {
        +getType()
    }
    
    %% Broken inheritance in original code!
    ElectricVehicle <.. ElectricCar : merely calls __init__
    ElectricVehicle <.. ElectricBike : merely calls __init__
    
    ParkingLot --> Vehicle : creates & stores
    ParkingLot --> ElectricVehicle : creates & stores
    ParkingLot --> ElectricCar : creates directly
    ParkingLot --> ElectricBike : creates directly
```

### 2. Behavioral Diagram (Sequence Diagram - Parking a Car)
This sequence diagram shows the flow of parking an Electric Car in the original code. The `ParkingLot` class directly handles the conditional logic to figure out which concrete class (`ElectricCar`, `ElectricBike`, `Car`, `Motorcycle`) to instantiate.

```mermaid
sequenceDiagram
    actor User
    participant GUI as Tkinter GUI (Global Scope)
    participant PL as ParkingLot
    participant EC as ElectricCar
    
    User->>GUI: Click "Park Car" (is_ev=1, motor=0)
    GUI->>PL: park(regnum, make, model, color, 1, 0)
    PL->>PL: check capacity (numOfOccupiedEvSlots < evCapacity)
    PL->>PL: getEmptyEvSlot()
    PL->>EC: new ElectricCar(regnum, make, model, color)
    EC-->>PL: instance
    PL->>PL: evSlots[slotid] = instance
    PL->>GUI: tfield.insert("Allocated slot...")
    PL-->>GUI: return slotid
```

---

## Part 2: Re-Designed Codebase

### 1. Structural Diagram (Class Diagram)
This diagram illustrates the refactored architecture. The `AppGUI` is cleanly separated from the `ParkingLot`. The `ParkingLot` supports the **Observer** pattern for trace/output notifications, so each facility can have independent state while UI or logging components subscribe to events. Furthermore, the `ParkingLot` no longer knows about concrete vehicle implementations; it delegates instantiation to the `VehicleFactory` (**Factory Method** pattern). The inheritance chain for Electric Vehicles has been corrected.

```mermaid
classDiagram
    class ParkingLot {
        +int capacity
        +int evCapacity
        +int level
        +list slots
        +list evSlots
        -list trace_observers
        +createParkingLot(...)
        +park(regnum, make, model, color, ev, motor, vehicle_type)
        +leave(slotid, ev)
        +add_trace_observer(observer)
        +remove_trace_observer(observer)
    }
    
    class VehicleFactory {
        +create_vehicle(is_ev, is_motorcycle, regnum, make, model, color, vehicle_type)$ Vehicle
    }
    
    class Vehicle {
        +string regnum
        +string make
        +string model
        +string color
        +string type
    }
    class Car
    class Truck
    class Motorcycle
    class Bus
    class ElectricVehicle {
        +int charge
        +setCharge(charge)
        +getCharge()
    }
    class ElectricCar
    class ElectricBike
    
    Vehicle <|-- Car
    Vehicle <|-- Truck
    Vehicle <|-- Motorcycle
    Vehicle <|-- Bus
    Vehicle <|-- ElectricVehicle
    ElectricVehicle <|-- ElectricCar
    ElectricVehicle <|-- ElectricBike
    
    ParkingLot ..> VehicleFactory : delegates to
    VehicleFactory ..> Car : instantiates
    VehicleFactory ..> Truck : instantiates
    VehicleFactory ..> Motorcycle : instantiates
    VehicleFactory ..> Bus : instantiates
    VehicleFactory ..> ElectricCar : instantiates
    VehicleFactory ..> ElectricBike : instantiates
    
    ParkingLot "1" *-- "*" Vehicle : stores in slots
    
    class AppGUI {
        -ParkingLot parkinglot
        -Tk root
        +create_widgets()
        +makeLot()
        +parkCar()
        +removeCar()
    }
    AppGUI --> ParkingLot : uses
    ParkingLot ..> AppGUI : notifies trace observer
```

### 2. Behavioral Diagram (Sequence Diagram - Parking a Car)
This sequence diagram shows the refactored flow. The GUI now interacts with the `ParkingLot`, which cleanly requests a vehicle instance from the `VehicleFactory`. The GUI is fully responsible for updating the display, and the `ParkingLot` simply returns the result data.

```mermaid
sequenceDiagram
    actor User
    participant GUI as AppGUI
    participant PL as ParkingLot
    participant VF as VehicleFactory
    participant EC as ElectricCar
    
    User->>GUI: Click "Park Car" (is_ev=1, motor=0)
    GUI->>PL: park(regnum, make, model, color, 1, 0, vehicle_type=None)
    PL->>PL: check capacity (numOfOccupiedEvSlots < evCapacity)
    PL->>PL: getEmptyEvSlot()
    PL->>VF: create_vehicle(is_ev=True, is_motorcycle=False, ...)
    VF->>EC: new ElectricCar(...)
    EC-->>VF: instance
    VF-->>PL: polymorphic Vehicle instance
    PL->>PL: evSlots[slotid] = instance
    PL-->>GUI: return slotid
    GUI->>GUI: write_output("Allocated slot number: [slotid]")
    GUI-->>User: Display output
```
