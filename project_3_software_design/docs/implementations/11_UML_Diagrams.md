# UML Diagrams (Original vs. Refactored)

As required by the project rubrics, here are the two sets of UML diagrams (Structural and Behavioral) representing the application before and after refactoring.

The Mermaid diagrams below are the canonical diagrams. PNG exports are stored in [`../../uml_diagrams/`](../../uml_diagrams/), but they should be regenerated from the `.mmd` sources if the Mermaid source changes.

To keep the diagrams readable, the class diagrams show the methods that explain the main design relationships. Routine getters, repeated search/query helpers, and simple report-formatting methods are described in notes instead of being listed one by one.

---

## Part 1: Original Codebase

### 1. Structural Diagram (Class Diagram)
This diagram illustrates the original, tightly coupled structure. Notice the broken inheritance chain where `ElectricCar` and `ElectricBike` call `ElectricVehicle.__init__()` but do not actually extend `ElectricVehicle`. The legacy `ParkingLot` also contains GUI callback methods and directly instantiates the supported concrete vehicle classes used by the manager.

```mermaid
classDiagram
    class ParkingLot {
        +int capacity
        +int evCapacity
        +int level
        +int numOfOccupiedSlots
        +int numOfOccupiedEvSlots
        +list slots
        +list evSlots
        +createParkingLot(capacity, evcapacity, level)
        +park(regnum, make, model, color, ev, motor)
        +leave(slotid, ev)
        +edit(slotid, regnum, make, model, color, ev)
        +parkCar()
        +removeCar()
        +makeLot()
    }
    note for ParkingLot "Also contains status, charge-status, slot search, query, and Tkinter output helper methods."

    class TkinterGlobals {
        <<global module state>>
        +Tk root
        +StringVar inputs
        +IntVar flags
        +Text tfield
        +main()
    }

    class Vehicle {
        +string regnum
        +string make
        +string model
        +string color
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

    ElectricVehicle <.. ElectricCar : calls __init__ only
    ElectricVehicle <.. ElectricBike : calls __init__ only

    TkinterGlobals --> ParkingLot : creates instance and binds buttons
    ParkingLot ..> TkinterGlobals : reads input vars and writes tfield
    ParkingLot --> Car : creates directly
    ParkingLot --> Motorcycle : creates directly
    ParkingLot --> ElectricCar : creates directly
    ParkingLot --> ElectricBike : creates directly
    ParkingLot "1" *-- "*" Vehicle : regular slots store Car/Motorcycle
    ParkingLot "1" *-- "*" ElectricCar : EV slots may store
    ParkingLot "1" *-- "*" ElectricBike : EV slots may store
```

*Source: [`../../uml_diagrams/original_class_diagram.mmd`](../../uml_diagrams/original_class_diagram.mmd)*

### 2. Behavioral Diagram (Sequence Diagram - Parking a Car)
This sequence diagram shows the flow of parking an Electric Car in the original code. The Tkinter button is bound to `ParkingLot.parkCar()`, which reads global Tkinter variables, calls `ParkingLot.park()`, and then writes the result to the global text field. The `ParkingLot` class directly handles the conditional logic to figure out which concrete class (`ElectricCar`, `ElectricBike`, `Car`, `Motorcycle`) to instantiate.

```mermaid
sequenceDiagram
    actor User
    participant GUI as Tkinter Button/Globals
    participant PL as ParkingLot
    participant EC as ElectricCar
    participant TF as Tkinter Text tfield

    User->>GUI: Click "Park Car" (is_ev=1, motor=0)
    GUI->>PL: parkCar()
    PL->>GUI: read reg/make/model/color/ev/motor StringVar and IntVar values
    PL->>PL: park(regnum, make, model, color, 1, 0)
    PL->>PL: check EV capacity
    PL->>PL: getEmptyEvSlot()
    PL->>EC: ElectricCar(regnum, make, model, color)
    EC-->>PL: electric car instance
    PL->>PL: evSlots[index] = instance
    PL-->>PL: return allocated slot number
    PL->>TF: insert("Allocated slot number: ...")
    GUI-->>User: Output appears in text field
```

*Source: [`../../uml_diagrams/original_sequence_diagram.mmd`](../../uml_diagrams/original_sequence_diagram.mmd)*

---

## Part 2: Re-Designed Codebase

### 1. Structural Diagram (Class Diagram)
This diagram illustrates the refactored architecture. The `AppGUI` is separated from the `ParkingLot` and owns the Tkinter state. The `ParkingLot` supports observer-style trace notifications, so UI or logging components can subscribe to domain events. Vehicle creation is delegated to `VehicleFactory`, which centralizes the concrete type decision for `Car`, `Truck`, `Motorcycle`, `Bus`, `ElectricCar`, and `ElectricBike`. The inheritance chain for electric vehicles has been corrected.

```mermaid
classDiagram
    class ParkingLot {
        +int capacity
        +int evCapacity
        +int level
        +int numOfOccupiedSlots
        +int numOfOccupiedEvSlots
        +list slots
        +list evSlots
        -list event_observers
        +createParkingLot(capacity, evcapacity, level)
        +park(regnum, make, model, color, ev, motor, vehicle_type)
        +leave(slotid, ev)
        +status()
        +chargeStatus()
        +set_pricing_strategy(strategy)
        +add_event_observer(observer)
        +remove_event_observer(observer)
        +publish(event)
    }
    note for ParkingLot "Still owns slot search and query helper methods. They are omitted here to keep the high-level class view readable."

    class VehicleFactory {
        +create_vehicle(is_ev, is_motorcycle, regnum, make, model, color, vehicle_type)
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

    class PricingStrategy {
        <<interface>>
        +calculate_fee(vehicle)
    }
    class FlatRateStrategy
    class EVPremiumStrategy
    class VehicleTypeStrategy
    PricingStrategy <|-- FlatRateStrategy
    PricingStrategy <|-- EVPremiumStrategy
    PricingStrategy <|-- VehicleTypeStrategy

    ParkingLot o-- PricingStrategy : strategy

    class DomainEvent {
        <<base class>>
        +datetime timestamp
    }
    class LotInitializedEvent
    class VehicleParkedEvent
    class VehicleDepartedEvent
    class VehicleParkFailedEvent

    DomainEvent <|-- LotInitializedEvent
    DomainEvent <|-- VehicleParkedEvent
    DomainEvent <|-- VehicleDepartedEvent
    DomainEvent <|-- VehicleParkFailedEvent

    ParkingLot ..> DomainEvent : publishes

    ParkingLot "1" *-- "*" Vehicle : stores in slots and evSlots

    class AppGUI {
        -ParkingLot parkinglot
        -Tk root
        +create_widgets()
        +makeLot()
        +parkCar()
        +removeCar()
        +write_output(text)
        -_handle_event(event)
    }
    note for AppGUI "Also contains UI handlers for search, status, charge status, and randomized sample input."
    class TkinterWidgets {
        <<GUI state>>
        +StringVar inputs
        +IntVar flags
        +Text output
        +Text trace
    }
    AppGUI --> ParkingLot : uses
    AppGUI --> TkinterWidgets : owns
    ParkingLot ..> AppGUI : notifies event observer callback
```

*Source: [`../../uml_diagrams/refactored_class_diagram.mmd`](../../uml_diagrams/refactored_class_diagram.mmd)*

### 2. Behavioral Diagram (Sequence Diagram - Parking a Car)
This sequence diagram shows the refactored flow. The GUI now interacts with the `ParkingLot`, which validates the request, checks for duplicate registrations, and requests a vehicle instance from `VehicleFactory`. The GUI is responsible for displaying the returned result, while trace messages are delivered through the registered observer callback.

```mermaid
sequenceDiagram
    actor User
    participant GUI as AppGUI
    participant PL as ParkingLot
    participant VF as VehicleFactory
    participant EC as ElectricCar
    participant EventBus as Event Observer

    User->>GUI: Click "Park Car" (is_ev=1, motor=0)
    GUI->>PL: park(regnum, make, model, color, 1, 0, vehicle_type=None)
    PL->>PL: validate registration number
    PL->>PL: getSlotNumFromRegNum(regnum, True)
    PL->>PL: getSlotNumFromRegNum(regnum, False)
    PL->>PL: check EV capacity
    PL->>PL: getEmptyEvSlot()
    PL->>VF: create_vehicle(True, False, regnum, make, model, color, vehicle_type=None)
    VF->>EC: ElectricCar(regnum, make, model, color)
    EC-->>VF: electric car instance
    VF-->>PL: polymorphic Vehicle instance
    PL->>PL: evSlots[index] = instance
    PL->>EventBus: publish(VehicleParkedEvent)
    PL-->>GUI: return allocated slot number
    GUI->>GUI: write_output("Allocated slot number: ...")
    GUI-->>User: Display output
```

*Source: [`../../uml_diagrams/refactored_sequence_diagram.mmd`](../../uml_diagrams/refactored_sequence_diagram.mmd)*
