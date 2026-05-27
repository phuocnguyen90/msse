# UML Diagrams (Original vs. Refactored)

As required by the project rubrics, here are the two sets of UML diagrams (Structural and Behavioral) representing the application before and after refactoring.

The Mermaid diagrams below are the canonical diagrams. PNG exports are stored in [`../../uml_diagrams/`](../../uml_diagrams/), but they should be regenerated from the `.mmd` sources if the Mermaid source changes.

To keep the diagrams readable, the class diagrams show the methods that explain the main design relationships. Routine getters, repeated search/query helpers, and simple report-formatting methods are described in notes instead of being listed one by one.

---

## Part 1: Original Codebase

### 1. Structural Diagrams (Class Diagrams)

The original architecture is shown as a set of focused diagrams, each highlighting a specific design problem.

#### a) High-Level System Overview
This diagram shows the monolithic structure: `ParkingLot` contains domain logic, GUI callbacks, query helpers, and direct Tkinter output code all in one class. Tkinter state lives as global module variables.

```mermaid
classDiagram
    class ParkingLot {
        +createParkingLot(capacity, evcapacity, level)
        +park(regnum, make, model, color, ev, motor)
        +leave(slotid, ev)
        +edit(slotid, regnum, make, model, color, ev)
        +parkCar()
        +removeCar()
        +makeLot()
    }
    note for ParkingLot "Domain logic, GUI callbacks, query helpers, and Tkinter output all in one class"

    class TkinterGlobals {
        <<global module state>>
        +Tk root
        +StringVar inputs
        +IntVar flags
        +Text tfield
        +main()
    }
    note for TkinterGlobals "Global variables at module level; ParkingLot reads/writes directly"

    TkinterGlobals --> ParkingLot : creates instance and binds buttons
    ParkingLot ..> TkinterGlobals : reads input vars and writes tfield
```

*Source: [`../../uml_diagrams/original_overview_diagram.mmd`](../../uml_diagrams/original_overview_diagram.mmd)*

#### b) Broken Inheritance
This diagram isolates the inheritance problem: `ElectricCar` and `ElectricBike` call `ElectricVehicle.__init__()` but do not formally declare `class ElectricCar(ElectricVehicle)`. They also duplicate getter methods already present in `Vehicle`.

```mermaid
classDiagram
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

    note for ElectricCar "Does NOT declare class ElectricCar(ElectricVehicle)"
    note for ElectricBike "Does NOT declare class ElectricBike(ElectricVehicle)"
    note for ElectricVehicle "Duplicate getters identical to Vehicle; no inheritance link"
```

*Source: [`../../uml_diagrams/original_broken_inheritance_diagram.mmd`](../../uml_diagrams/original_broken_inheritance_diagram.mmd)*

#### c) Direct Instantiation
This diagram isolates the concrete-class coupling: `ParkingLot` directly instantiates `Car`, `Motorcycle`, `ElectricCar`, and `ElectricBike` inside deeply nested `if/else` logic. There is no creation abstraction.

```mermaid
classDiagram
    class ParkingLot {
        +park(regnum, make, model, color, ev, motor)
        +leave(slotid, ev)
    }
    note for ParkingLot "Deeply nested if/else inside park() to choose concrete class"

    class Car {
        +getType()
    }
    class Motorcycle {
        +getType()
    }
    class ElectricCar {
        +getType()
    }
    class ElectricBike {
        +getType()
    }

    ParkingLot --> Car : new Car(...)
    ParkingLot --> Motorcycle : new Motorcycle(...)
    ParkingLot --> ElectricCar : new ElectricCar(...)
    ParkingLot --> ElectricBike : new ElectricBike(...)

    ParkingLot "1" *-- "*" Car : stores in regular slots
    ParkingLot "1" *-- "*" Motorcycle : stores in regular slots
    ParkingLot "1" *-- "*" ElectricCar : stores in EV slots
    ParkingLot "1" *-- "*" ElectricBike : stores in EV slots

    note for ParkingLot "No creation abstraction; directly references every concrete class"
```

*Source: [`../../uml_diagrams/original_direct_instantiation_diagram.mmd`](../../uml_diagrams/original_direct_instantiation_diagram.mmd)*

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

### 1. Structural Diagrams (Class Diagrams)

The refactored architecture is shown as a set of focused diagrams rather than one overloaded class diagram. This mirrors the DDD bounded-context approach used elsewhere in the documentation.

#### a) High-Level System Overview
This diagram shows the main architectural components and their responsibilities at a glance.

```mermaid
classDiagram
    class ParkingLot {
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
    note for ParkingLot "Owns slot state, queries, and delegates to collaborators"

    class AppGUI {
        +create_widgets()
        +makeLot()
        +parkCar()
        +removeCar()
        +write_output(text)
        -_handle_event(event)
    }
    note for AppGUI "Owns Tkinter state and subscribes to domain events"

    class VehicleFactory {
        +create_vehicle(...)
    }
    note for VehicleFactory "Centralizes vehicle creation"

    class PricingStrategy {
        <<interface>>
        +calculate_fee(vehicle)
    }
    note for PricingStrategy "Pluggable pricing models"

    class DomainEvent {
        <<base>>
        +datetime timestamp
    }
    note for DomainEvent "Typed events for audit and integration"

    AppGUI --> ParkingLot : uses
    ParkingLot ..> VehicleFactory : delegates creation
    ParkingLot o-- PricingStrategy : composes
    ParkingLot ..> DomainEvent : publishes
    AppGUI ..> ParkingLot : subscribes to events
```

*Source: [`../../uml_diagrams/refactored_overview_diagram.mmd`](../../uml_diagrams/refactored_overview_diagram.mmd)*

#### b) Vehicle & Factory Hierarchy
This diagram focuses on the inheritance tree and the Factory Method pattern.

```mermaid
classDiagram
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

    VehicleFactory ..> Car : instantiates
    VehicleFactory ..> Truck : instantiates
    VehicleFactory ..> Motorcycle : instantiates
    VehicleFactory ..> Bus : instantiates
    VehicleFactory ..> ElectricCar : instantiates
    VehicleFactory ..> ElectricBike : instantiates

    note for Vehicle "Dynamic type property derived from class name"
    note for ElectricCar "Overrides type as 'Car' for parking categorization"
    note for ElectricBike "Overrides type as 'Motorcycle' for parking categorization"
```

*Source: [`../../uml_diagrams/refactored_vehicle_factory_diagram.mmd`](../../uml_diagrams/refactored_vehicle_factory_diagram.mmd)*

#### c) Event-Driven Architecture
This diagram focuses on the Observer / Event-Driven pattern and the typed domain event hierarchy.

```mermaid
classDiagram
    class ParkingLot {
        -list event_observers
        +add_event_observer(observer)
        +remove_event_observer(observer)
        +publish(event)
    }

    class DomainEvent {
        <<base class>>
        +datetime timestamp
    }
    class LotInitializedEvent {
        +int capacity
        +int ev_capacity
        +int level
    }
    class VehicleParkedEvent {
        +Vehicle vehicle
        +int slot_id
        +bool is_ev
    }
    class VehicleDepartedEvent {
        +Vehicle vehicle
        +int slot_id
        +bool is_ev
        +float fee
    }
    class VehicleParkFailedEvent {
        +string reason
    }
    class VehicleDepartFailedEvent {
        +string reason
    }
    class PricingStrategyChangedEvent {
        +string strategy_name
    }

    DomainEvent <|-- LotInitializedEvent
    DomainEvent <|-- VehicleParkedEvent
    DomainEvent <|-- VehicleDepartedEvent
    DomainEvent <|-- VehicleParkFailedEvent
    DomainEvent <|-- VehicleDepartFailedEvent
    DomainEvent <|-- PricingStrategyChangedEvent

    ParkingLot ..> DomainEvent : publishes

    note for ParkingLot "Synchronous in-process observer list. Future: async message broker"
    note for DomainEvent "Strongly typed events replace brittle string traces"
```

*Source: [`../../uml_diagrams/refactored_event_system_diagram.mmd`](../../uml_diagrams/refactored_event_system_diagram.mmd)*

#### d) Pricing Strategy
This diagram focuses on the Strategy pattern for pluggable fee calculation.

```mermaid
classDiagram
    class ParkingLot {
        +set_pricing_strategy(strategy)
        +leave(slotid, ev)
    }
    note for ParkingLot "Delegates fee calculation to strategy at departure"

    class PricingStrategy {
        <<interface>>
        +calculate_fee(vehicle)
    }
    class FlatRateStrategy {
        +float rate
        +calculate_fee(vehicle)
    }
    class EVPremiumStrategy {
        +float base_rate
        +float ev_surcharge
        +calculate_fee(vehicle)
    }
    class VehicleTypeStrategy {
        +float motorcycle_rate
        +float car_rate
        +float truck_bus_rate
        +float ev_surcharge
        +calculate_fee(vehicle)
    }

    PricingStrategy <|-- FlatRateStrategy
    PricingStrategy <|-- EVPremiumStrategy
    PricingStrategy <|-- VehicleTypeStrategy

    ParkingLot o-- PricingStrategy : strategy

    note for FlatRateStrategy "Fixed fee regardless of vehicle type"
    note for EVPremiumStrategy "Base rate + EV surcharge via duck typing"
    note for VehicleTypeStrategy "Differentiated by vehicle.type + EV surcharge"
```

*Source: [`../../uml_diagrams/refactored_pricing_strategy_diagram.mmd`](../../uml_diagrams/refactored_pricing_strategy_diagram.mmd)*

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
