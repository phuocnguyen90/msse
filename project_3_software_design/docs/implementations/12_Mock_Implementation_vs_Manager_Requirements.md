# Mock Implementation vs. Technical Manager Requirements

The current mock implementation serves as a foundational prototype. While it does not include the full microservices architecture yet, it intentionally addresses several core business rules and operational requirements raised by Michael (Technical Manager) in the interview. 

Here is how the mock implementation ([`refactored_code/ParkingManager.py`](../../refactored_code/ParkingManager.py), [`refactored_code/AppGUI.py`](../../refactored_code/AppGUI.py), and [`refactored_code/VehicleFactory.py`](../../refactored_code/VehicleFactory.py)) conceptually maps to the real-world problems discussed:

## 1. EV Charging Station Management (New Domain)

**Manager's Problem:** 
EV chargers are tied to specific designated parking spots, not spread across the whole facility. Non-EVs shouldn't park there. The system needs to track charging statuses.

**Mock Implementation Address:**
* **Designated Spots:** The `ParkingLot` class explicitly separates capacity into `capacity` (regular) and `evCapacity` (EV-only). It maintains two separate arrays: `slots` and `evSlots`. 
* **Slot Routing:** The `park()` method uses an `ev` boolean flag to route vehicles to regular or EV-only slot collections. This is a simplified version of the designated EV bay rule; a production system would add stronger validation between vehicle type, charger assignment, and physical bay occupancy.
* **EV-Specific Status Placeholder:** The `chargeStatus()` method iterates specifically over `evSlots` to report the current `charge %` of parked electric vehicles. This does not fully implement charger states such as Available, Charging, Faulted, or Offline, but it creates a placeholder for EV-specific operational status reporting.

## 2. Local Offline Autonomy

**Manager's Problem:** 
Facilities must remain operational (barriers, occupancy, ticketing) even if they lose internet connection to the central servers.

**Mock Implementation Address:**
* **Edge Node Simulation:** Each `ParkingLot` instance maintains its own local state (`slots`, `evSlots`, `numOfOccupiedSlots`, and `numOfOccupiedEvSlots`) in memory. This models the idea that each facility edge node can keep operating with independent local state.
* **Local Processing:** Operations like `park()` and `leave()` execute locally without requiring network calls. This proves the concept that a facility edge node can track occupancy and manage entry/exit autonomously during an internet outage.

## 3. Domain & Ubiquitous Language

**Manager's Problem:** 
Tracking a vehicle's stay from entry to exit ("Parking Session"), including handling physical/digital access credentials ("Tickets").

**Mock Implementation Address:**
* **Session Placeholder:** When `park()` is called, the system allocates a slot and returns a `slotid`. This `slotid` acts as a simplified stand-in for a local "Ticket" or parking-session identifier.
* **Exit Processing:** To end the simplified session, `leave(slotid, ev)` must be called with the matching slot identifier. The mock demonstrates the entry-to-exit lifecycle, while the full domain model would also track entry time, exit time, status, customer/account references, payment state, and history.

## 4. Reservations & Capacity Management

**Manager's Problem:** 
Facilities run in a "degraded mode" during outages, relying on local capacity tracking to ensure reservations and drive-ups don't conflict, using reserved capacity buffers.

**Mock Implementation Address:**
* **Strict Occupancy Tracking:** The system meticulously tracks `numOfOccupiedSlots` and `numOfOccupiedEvSlots` against `capacity` and `evCapacity`. 
* **Buffer Foundation:** It rejects `park()` requests when the relevant capacity is full. This provides a starting point for a future reserved-capacity buffer, but the mock does not yet implement reservations, priority rules, degraded mode, or conflict reconciliation.

## 5. Traceability and Auditability

**Manager's Problem:** 
We need event streaming and audit trails for cross-facility reporting and transactions.

**Mock Implementation Address:**
* **Event Tracing:** The `ParkingLot` implements an observer-based `_trace()` mechanism. Key actions such as `createParkingLot`, `park`, `leave`, status queries, and factory-created vehicles can emit timestamped trace messages to subscribed observers. In the future microservices architecture, this local tracing mechanism maps conceptually to publishing domain events to a message broker such as Kafka for central analytics and eventual consistency.

## 6. Facility Variability and Vehicle Types

**Manager's Problem:**
Different facilities can have different business rules, access mechanisms, and operational needs. The prototype should be easy to extend without adding more conditional logic directly inside `ParkingLot`.

**Mock Implementation Address:**
* **Factory-Based Extensibility:** `VehicleFactory.create_vehicle()` centralizes vehicle construction. Existing calls support regular cars, motorcycles, electric cars, and electric bikes through the original flags, while the optional `vehicle_type` parameter supports additional regular vehicle categories such as trucks and buses.
* **Reduced Coupling:** `ParkingLot` delegates vehicle creation to the factory instead of directly instantiating each concrete vehicle class. This makes it easier to add facility-specific vehicle policies later without scattering construction logic across the parking workflow.
