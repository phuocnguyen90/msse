# EasyParkPlus Software Design & Architecture Final Report

## 1. Project Overview

This report presents the refactored EasyParkPlus parking lot management prototype and the proposed target architecture for scaling the system across multiple facilities with Electric Vehicle (EV) Charging Station Management.

The original codebase was a single-lot Tkinter prototype. The project work focused on:

- Reviewing the original code for poor design, coding problems, and anti-patterns.
- Refactoring the code with appropriate object-oriented design patterns.
- Representing both the original and redesigned code with UML diagrams.
- Extending the system conceptually with Domain-Driven Design (DDD).
- Proposing a preliminary microservices architecture for multi-facility EV charging operations.
- Documenting remaining prototype limitations and technical debt.

The submitted package keeps the detailed source documents in `docs/implementations/` and `docs/requirements/`. This final report is the cohesive presentation document for grading.

## 2. AI Usage Disclosure

I used AI coding tools, including Codex and Antigravity, as part of an AI-assisted software development lifecycle. I personally directed the work by defining the project goals, planning the implementation steps, reviewing requirements, and deciding what changes should be made.

The AI agents were used to help execute specific development tasks, including code refactoring, documentation drafting, diagram updates, test creation, and running verification checks. After each iteration, I manually reviewed the AI-generated work, evaluated whether it matched the project requirements, requested corrections where needed, and approved the final direction.

I remain responsible for the final submission. AI tools were used as implementation and review assistants, but I supervised the process, reviewed outputs, validated changes against the project requirements, and iterated on the work until the final product was ready.

## 3. Refactoring Summary

### 3.1 Original Design Problems

The original implementation had design problems at several levels:

- **Paradigm-level OOP problems:** weak responsibility assignment, broken inheritance, concrete-class coupling, and primitive flags used in place of clearer domain concepts.
- **Design anti-patterns:** a Smart UI style where domain logic depended on global Tkinter variables, and a `ParkingLot` class that was trending toward a God Object.
- **Maintainability problems:** duplicated code, dead code, unused imports, repeated query methods, hardcoded type strings, and mixed sentinel values with domain objects.
- **Defect risks:** inverted motorcycle/car creation logic, inconsistent slot indexing, missing bounds validation, unhandled input conversion errors, and buggy copy-paste methods.

The key issue was not just that the original code had individual bugs. The larger design problem was that the application lacked clear abstraction and service boundaries: UI control, domain state, object construction, output formatting, and query behavior were all concentrated in one module/class.

### 3.2 Refactoring Goals

The refactor aimed to:

- Separate Tkinter presentation behavior from parking domain behavior.
- Move vehicle creation out of `ParkingLot`.
- Fix the EV inheritance hierarchy.
- Preserve the original query and parking behavior where appropriate.
- Add support for trucks and buses through the same creation abstraction.
- Introduce testable extension points for pricing and domain events.
- Keep the prototype honest by documenting remaining limitations rather than claiming full production readiness.

### 3.3 Implemented Design Patterns

#### Simple Factory / Factory Method-Style Creation

Vehicle creation was extracted into `VehicleFactory.create_vehicle(...)`. This is technically closer to a Simple Factory than the strict Gang of Four Factory Method pattern because the implementation uses a centralized static creator instead of subclass-defined factory methods.

The factory supports:

- `Car`
- `Motorcycle`
- `Truck`
- `Bus`
- `ElectricCar`
- `ElectricBike`

The `ParkingLot` no longer directly constructs every concrete vehicle class.

#### Observer Pattern / Event-Driven Scaffolding

The original code directly wrote to a Tkinter text field from domain methods. The refactored code instead uses typed domain events and an observer list:

- `ParkingLot.add_event_observer(observer)`
- `ParkingLot.remove_event_observer(observer)`
- `ParkingLot.publish(event)`

The GUI subscribes to the domain events and displays them. This is not a full production event broker, but it is an event-driven scaffold that decouples the domain logic from presentation behavior.

Implemented event types include:

- `LotInitializedEvent`
- `VehicleParkedEvent`
- `VehicleDepartedEvent`
- `VehicleParkFailedEvent`
- `VehicleDepartFailedEvent`
- `PricingStrategyChangedEvent`

#### Strategy Pattern for Pricing

Parking fee calculation was extracted into a `PricingStrategy` interface with concrete strategies:

- `FlatRateStrategy`
- `EVPremiumStrategy`
- `VehicleTypeStrategy`

`ParkingLot` delegates fee calculation during `leave(...)`, so the pricing rule can change without rewriting the parking workflow.

### 3.4 Remaining Refactoring Limitations

The refactor improves the prototype but does not fully convert it into a production-grade domain model. Known limitations include:

- `ParkingLot` still owns query helpers and display-oriented report string generation.
- Public methods still use primitive flags such as `ev` and `motor`.
- There is no `ParkingSession` aggregate in the running prototype.
- EV charging is represented only through `evSlots` and a simple `charge` attribute.
- The GUI still manages only one active `ParkingLot` instance at a time.

These limitations are documented intentionally in the technical debt section rather than hidden.

## 4. UML Diagrams

The UML diagrams are split into focused diagrams because a single large class diagram became difficult to read. The source Mermaid files and PNG exports are stored in `uml_diagrams/`.

### 4.1 Original Codebase Diagrams

#### Original High-Level Structure

The original system combines domain logic, GUI callbacks, query helpers, and direct Tkinter output in `ParkingLot`.

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

#### Original Broken Inheritance

```mermaid
classDiagram
    class Vehicle
    class Car
    class Truck
    class Motorcycle
    class Bus
    Vehicle <|-- Car
    Vehicle <|-- Truck
    Vehicle <|-- Motorcycle
    Vehicle <|-- Bus

    class ElectricVehicle
    class ElectricCar
    class ElectricBike

    ElectricVehicle <.. ElectricCar : calls __init__ only
    ElectricVehicle <.. ElectricBike : calls __init__ only

    note for ElectricCar "Does NOT declare class ElectricCar(ElectricVehicle)"
    note for ElectricBike "Does NOT declare class ElectricBike(ElectricVehicle)"
```

#### Original Parking Sequence

```mermaid
sequenceDiagram
    actor User
    participant GUI as Tkinter Button/Globals
    participant PL as ParkingLot
    participant EC as ElectricCar
    participant TF as Tkinter Text tfield

    User->>GUI: Click "Park Car" (is_ev=1, motor=0)
    GUI->>PL: parkCar()
    PL->>GUI: read global Tkinter variables
    PL->>PL: park(regnum, make, model, color, 1, 0)
    PL->>PL: getEmptyEvSlot()
    PL->>EC: ElectricCar(regnum, make, model, color)
    EC-->>PL: electric car instance
    PL->>PL: evSlots[index] = instance
    PL->>TF: insert("Allocated slot number: ...")
    GUI-->>User: Output appears in text field
```

### 4.2 Refactored Codebase Diagrams

#### Refactored High-Level Structure

```mermaid
classDiagram
    class ParkingLot {
        +createParkingLot(capacity, evcapacity, level)
        +park(regnum, make, model, color, ev, motor, vehicle_type)
        +leave(slotid, ev)
        +set_pricing_strategy(strategy)
        +add_event_observer(observer)
        +remove_event_observer(observer)
        +publish(event)
    }
    note for ParkingLot "Owns slot state, queries, and delegates to collaborators"

    class AppGUI {
        +makeLot()
        +parkCar()
        +removeCar()
        +write_output(text)
        -_handle_event(event)
    }
    note for AppGUI "Owns Tkinter state and subscribes to domain events"

    class VehicleFactory
    class PricingStrategy
    class DomainEvent

    AppGUI --> ParkingLot : uses
    ParkingLot ..> VehicleFactory : delegates creation
    ParkingLot o-- PricingStrategy : composes
    ParkingLot ..> DomainEvent : publishes
    AppGUI ..> ParkingLot : subscribes to events
```

#### Refactored Vehicle and Factory Hierarchy

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
```

#### Refactored Event System

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
    class LotInitializedEvent
    class VehicleParkedEvent
    class VehicleDepartedEvent
    class VehicleParkFailedEvent
    class VehicleDepartFailedEvent
    class PricingStrategyChangedEvent

    DomainEvent <|-- LotInitializedEvent
    DomainEvent <|-- VehicleParkedEvent
    DomainEvent <|-- VehicleDepartedEvent
    DomainEvent <|-- VehicleParkFailedEvent
    DomainEvent <|-- VehicleDepartFailedEvent
    DomainEvent <|-- PricingStrategyChangedEvent

    ParkingLot ..> DomainEvent : publishes
    note for ParkingLot "Synchronous in-process observer list. Future: async message broker"
```

#### Refactored Parking Sequence

```mermaid
sequenceDiagram
    actor User
    participant GUI as AppGUI
    participant PL as ParkingLot
    participant VF as VehicleFactory
    participant EC as ElectricCar
    participant Obs as event_observers

    User->>GUI: Click "Park Car" (is_ev=1, motor=0)
    GUI->>PL: park(regnum, make, model, color, 1, 0, vehicle_type=None)
    PL->>PL: validate registration number
    PL->>PL: check duplicate registration
    PL->>PL: getEmptyEvSlot()
    PL->>VF: create_vehicle(True, False, regnum, make, model, color, vehicle_type=None)
    VF->>EC: ElectricCar(regnum, make, model, color)
    EC-->>VF: electric car instance
    VF-->>PL: polymorphic Vehicle instance
    PL->>PL: evSlots[index] = instance
    PL->>Obs: publish(VehicleParkedEvent)
    PL-->>GUI: return allocated slot number
    GUI->>GUI: write_output("Allocated slot number: ...")
    GUI-->>User: Display output
```

## 5. Domain-Driven Design

The DDD model is based on the project requirement to scale EasyParkPlus across multiple facilities and add EV Charging Station Management. Additional assumptions were informed by a technical-manager interview document.

### 5.1 Core Domain and Subdomains

**Core Domain:** Integrated Parking Management and EV Charging Management.

**Core Subdomains:**

- Access Control & Parking Sessions
- EV Charging Station Management

**Supporting Subdomains:**

- Reservations and Space Inventory
- Customer Accounts & Memberships
- Pricing & Tariff Management
- Settlement & Clearing

**Generic Subdomains:**

- Payment Processing
- Reporting, Finance, and Audits
- Maintenance & Asset Management

### 5.2 Bounded Contexts

```mermaid
flowchart TD
    subgraph "Core Domain"
        APC["Facility / Parking Context"]
        EVC["EV Charging Context"]
    end

    subgraph "Supporting Subdomains"
        CAC["Customer & Account Context"]
        RIC["Reservation & Inventory Context"]
        PTC["Pricing & Tariff Context"]
        SCC["Settlement & Clearing Context"]
    end

    subgraph "Generic Subdomains"
        PAY["Payment Processing Context"]
        RAF["Reporting / Audit Context"]
        MAC["Maintenance Context"]
    end
```

The Facility / Parking Context and EV Charging Context both require edge and cloud capabilities because garages must continue operating during internet outages.

### 5.3 Key Domain Models

#### Facility / Parking

- **Aggregate Root:** `ParkingSession`
- **Entities:** `Ticket`, `VehicleSnapshot`, `AccessDecision`
- **Value Objects:** `LicensePlate`, `Duration`, `EntryCredential`, `ParkingRateSnapshot`
- **Invariant:** A session must have one entry event before exit, and duplicate active sessions for the same license plate and facility are rejected.

#### Facility Inventory

- **Aggregate Root:** `FacilityInventory`
- **Entities:** `ParkingSpot`, `Gate`, `FacilityRuleOverride`
- **Value Objects:** `CapacityCount`, `SpotType`, `GateStatus`
- **Invariant:** Drive-up entries must not consume reserved capacity allocated for future reservations.

#### EV Charging

- **Aggregate Root:** `ChargingSession`
- **Entities:** `ChargingMeterReading`, `IdleFeeAssessment`
- **Value Objects:** `EnergyConsumed`, `IdleDuration`, `ConnectorID`, `ChargingTariffSnapshot`
- **Invariant:** A charging session must be linked to a designated EV bay.

#### Charger Asset

- **Aggregate Root:** `ChargerAsset`
- **Entities:** `Connector`, `MaintenanceState`
- **Value Objects:** `PowerRating`, `OcppEndpoint`, `HeartbeatTimestamp`
- **Invariant:** Each connector can serve only one active charging session at a time.

#### Billing and Settlement

- **Aggregate Root:** `UnifiedInvoice`
- **Entities:** `PaymentTransaction`
- **Value Objects:** `ChargeLineItem`, `Money`, `TaxBreakdown`, `PaymentMethodToken`
- **Rule:** Parking and charging may be presented as one customer receipt while preserving separate line items for tax, refund, and settlement.

- **Aggregate Root:** `SettlementBatch`
- **Entities:** `LedgerEntry`, `VendorInvoiceMatch`, `Adjustment`
- **Value Objects:** `RevenueShareRule`, `GrossAmount`, `NetAmount`
- **Rule:** Third-party charger revenue, landlord shares, idle fees, refunds, and adjustments must be reconciled from session-level records.

## 6. Proposed Microservices Architecture

The microservices architecture is a target-state architecture, not an implementation requirement for this prototype. It is intentionally broader than the current code because the real EasyParkPlus system must support multiple facilities, offline operation, EV hardware, payments, reservations, and financial settlement.

### 6.1 High-Level Architecture

```mermaid
flowchart TD
    Client["Mobile App & Web Clients"] --> API["API Gateway"]

    subgraph "Facility Edge Network"
        FS["Facility Edge Service"]
        LocalDevices["Gates, LPR, Kiosks, Local Chargers"]
        FS --- LocalDevices
    end

    subgraph "Cloud Infrastructure"
        API --> Parking["Facility / Parking"]
        API --> Reservation["Reservation"]
        API --> Charging["EV Charging"]
        API --> Customer["Customer Identity"]
        API --> Billing["Billing & Payment"]
        Settlement["Settlement"]
    end

    FS <-.->|"offline sync / operational APIs"| Parking
    Charging <-.->|"OCPP / vendor APIs"| ChargerNetwork["EV Charger Networks"]
    Billing <-.->|"payment API"| PaymentGateway["Payment Gateway"]
    Billing --> Settlement
```

### 6.2 Services and Responsibilities

- **Facility Edge Service:** Runs locally in each garage, controls gates, processes LPR/tickets, records offline events, and continues operation during outages.
- **Facility / Parking Service:** Owns cloud-side facility configuration, parking sessions, occupancy summaries, and cross-facility parking history.
- **EV Charging Service:** Integrates with chargers through OCPP/vendor APIs and tracks charging sessions and charger status.
- **Customer Identity Service:** Owns customer profiles, authentication, monthly subscriptions, saved payment methods, and vehicle profiles.
- **Billing & Payment Service:** Calculates combined parking and charging charges, integrates with payment gateways, and produces unified invoices.
- **Reservation Service:** Manages bookings, capacity buffers, future availability, and coordination with live occupancy.
- **Settlement Service:** Reconciles revenue sharing between EasyParkPlus, third-party charger operators, and landlords.

### 6.3 Database per Service

- **Facility Edge Service:** Local PostgreSQL for offline transactional durability.
- **Facility / Parking Service:** PostgreSQL for facility, parking-session, and occupancy records.
- **EV Charging Service:** MongoDB for charger telemetry and status records.
- **Customer Identity Service:** PostgreSQL for user and account data.
- **Billing & Payment Service:** CockroachDB or HA PostgreSQL for financial consistency.
- **Reservation Service:** Redis for fast locking/availability plus PostgreSQL for confirmed bookings.
- **Settlement Service:** Snowflake or equivalent warehouse for batch analytics and reconciliation.

### 6.4 API and Event Examples

External API examples:

- `GET /api/v1/facilities`
- `GET /api/v1/facilities/{facilityId}/occupancy`
- `POST /api/v1/parking-sessions`
- `POST /api/v1/parking-sessions/{sessionId}/exit-request`
- `POST /api/v1/reservations`
- `GET /api/v1/chargers?facilityId={id}`
- `POST /api/v1/charging/sessions`
- `GET /api/v1/invoices/history`

Internal synchronous examples:

- `POST /internal/facilities/{facilityId}/entry-decision`
- `POST /internal/facilities/{facilityId}/exit-decision`
- `POST /internal/billing/calculate`
- `GET /internal/pricing/tariffs?facilityId={id}`
- `POST /internal/sync/facilities/{facilityId}/reconcile`

Asynchronous event examples:

- `Facility.VehicleEntered`
- `Facility.VehicleExited`
- `Facility.OfflineTransactionRecorded`
- `Reservation.Confirmed`
- `ParkingSession.PaymentRequired`
- `Charger.SessionEnded`
- `Charger.StatusChanged`
- `Billing.PaymentCompleted`
- `Settlement.BatchClosed`

### 6.5 DevOps and Rollout Justification

The proposed architecture should be implemented incrementally:

1. Keep the refactored parking application as the core prototype.
2. Introduce a Facility Edge Service and cloud Facility / Parking Service.
3. Add Customer Identity, Billing & Payment, and Reservation services.
4. Add EV Charging integration through OCPP/vendor adapters.
5. Add Settlement, reporting, and finance workflows.

DevOps practices should include CI/CD, contract tests, event schema versioning, observability, feature flags, infrastructure as code, and rollback-friendly edge deployments.

## 7. Prototype Limitations and Technical Debt

The submitted implementation is a refactored prototype, not the full target architecture. The main gaps are:

| Area | Prototype Scaffolding | Missing for Production |
|------|----------------------|------------------------|
| EV Charging | `evSlots`, `chargeStatus()` | Charger state machine, OCPP, EV-bay enforcement |
| Offline Autonomy | In-memory local state | Persistent edge DB, sync, conflict reconciliation |
| Parking Sessions | `slotid` primitive | `ParkingSession` aggregate, timestamps, customer linkage |
| Reservations | Capacity counters | Reservation entity, priority rules, reserved buffers |
| Event Streaming | Typed in-process `DomainEvent` classes | Async broker, event store, schema versioning |
| Facility Variability | Strategy + Factory extension points | Multi-facility config, hardware adapters |
| Billing & Settlement | `PricingStrategy` hierarchy | Duration pricing, unified invoice, payment gateway |
| Security | Basic validation | Auth, RBAC, transactional slot locking |

These limitations are acceptable for a course prototype because the project asks for a refactored application plus architecture documentation, not a full production implementation.

## 8. Testing and Verification

The refactored code includes unit tests for:

- Vehicle properties and inheritance.
- Vehicle factory creation and validation.
- Parking lot creation, parking, leaving, queries, and bounds checks.
- Domain event publication.
- Pricing strategy behavior.

Verification command:

```bash
cd project_3_software_design
python -m unittest discover -s refactored_code -p "test_*.py"
```

Latest verified result:

```text
Ran 55 tests
OK
```

## 9. Requirement Traceability

| Requirement | Where Addressed |
|-------------|-----------------|
| Identify and improve bad coding practices | Refactoring Summary; detailed source doc `09_Refactoring_Justification.md` |
| Use at least two OO design patterns | Factory-style creation, Observer/event scaffolding, Strategy |
| UML for original design | Section 4.1 and `docs/implementations/11_UML_Diagrams.md` |
| UML for redesigned code | Section 4.2 and `docs/implementations/11_UML_Diagrams.md` |
| Written justification for changes and patterns | Sections 3 and 4; detailed source doc `09_Refactoring_Justification.md` |
| DDD core domains and bounded contexts | Section 5; detailed source doc `08_Domain_Driven_Design.md` |
| Basic domain models for parking and EV charging | Section 5.3 |
| Microservices architecture diagram | Section 6.1 |
| Services and responsibilities | Section 6.2 |
| APIs/endpoints | Section 6.4 |
| Separate DBs per service | Section 6.3 |
| Updated source code | `refactored_code/` |
| Screenshots/application evidence | `assets/Screenshot 2026-05-27 145128.png` |
| Prototype limitations vs. real requirements | Section 7; detailed source doc `12_Mock_Implementation_vs_Manager_Requirements.md` |

## 10. Submission Contents

The final project package should include:

- `refactored_code/` with updated source code and tests.
- `legacy_code/` for comparison against the original prototype.
- `uml_diagrams/` with Mermaid sources and PNG exports.
- `docs/Final_Report.md` as the main cohesive report.
- `docs/implementations/` as supporting detailed documentation.
- `docs/requirements/` as preserved requirement/rubric material.
- `assets/` with screenshot evidence of the application running.

