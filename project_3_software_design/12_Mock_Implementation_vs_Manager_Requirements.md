# Mock Implementation vs. Technical Manager Requirements

The current mock implementation serves as a foundational prototype. While it does not include the full microservices architecture yet, it intentionally addresses several core business rules and operational requirements raised by Michael (Technical Manager) in the interview. 

Here is how the mock implementation (`ParkingManager.py`, `AppGUI.py`, and `VehicleFactory.py`) conceptually maps to the real-world problems discussed:

## 1. EV Charging Station Management (New Domain)

**Manager's Problem:** 
EV chargers are tied to specific designated parking spots, not spread across the whole facility. Non-EVs shouldn't park there. The system needs to track charging statuses.

**Mock Implementation Address:**
* **Designated Spots:** The `ParkingLot` class explicitly separates capacity into `capacity` (regular) and `evCapacity` (EV-only). It maintains two separate arrays: `slots` and `evSlots`. 
* **Validation:** The `park()` method uses an `ev` boolean flag to strictly route vehicles to their designated spot type, ensuring a regular car cannot accidentally take an `evSlot`.
* **State Tracking:** The `chargeStatus()` method iterates specifically over `evSlots` to report the current `charge %` of parked electric vehicles, mirroring the requirement to track charger states.

## 2. Local Offline Autonomy

**Manager's Problem:** 
Facilities must remain operational (barriers, occupancy, ticketing) even if they lose internet connection to the central servers.

**Mock Implementation Address:**
* **Edge Node Simulation:** The `ParkingLot` is implemented as a local Singleton. All state (`slots`, `numOfOccupiedSlots`) is maintained locally in memory. 
* **Local Processing:** Operations like `park()` and `leave()` execute locally without requiring network calls. This proves the concept that a facility edge node can track occupancy and manage entry/exit autonomously during an internet outage.

## 3. Domain & Ubiquitous Language

**Manager's Problem:** 
Tracking a vehicle's stay from entry to exit ("Parking Session"), including handling physical/digital access credentials ("Tickets").

**Mock Implementation Address:**
* **Session Tracking:** When `park()` is called, the system allocates a slot and returns a `slotid`. This `slotid` acts as the local "Ticket" or session identifier.
* **Exit Processing:** To end the session, `leave(slotid, ev)` must be called with the matching ticket, accurately simulating the lifecycle of a Parking Session.

## 4. Reservations & Capacity Management

**Manager's Problem:** 
Facilities run in a "degraded mode" during outages, relying on local capacity tracking to ensure reservations and drive-ups don't conflict, using reserved capacity buffers.

**Mock Implementation Address:**
* **Strict Occupancy Tracking:** The system meticulously tracks `numOfOccupiedSlots` and `numOfOccupiedEvSlots` against `capacity` and `evCapacity`. 
* **Buffer Foundation:** It strictly rejects `park()` requests when `numOfOccupiedSlots >= capacity`. This rigid tracking provides the exact foundation needed to implement the "capacity buffer" (e.g., rejecting walk-ins when `numOfOccupiedSlots >= capacity - buffer`).

## 5. Traceability and Auditability

**Manager's Problem:** 
We need event streaming and audit trails for cross-facility reporting and transactions.

**Mock Implementation Address:**
* **Event Tracing:** The `ParkingLot` implements a robust `_trace()` callback mechanism. Every critical action (`__new__`, `createParkingLot`, `park`, `leave`) emits a timestamped event. In the future microservices architecture, this local tracing mechanism maps directly to publishing events to a message broker (like Kafka) for central analytics and eventual consistency.
