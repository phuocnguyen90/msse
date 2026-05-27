# Technical Debt Register: Mock Implementation vs. Manager Requirements

This document tracks the gap between the current prototype implementation and the real-world requirements raised by Michael (Technical Manager) in the technical interview. The prototype intentionally takes on technical debt to stay within project scope; each item below describes the debt, its business impact, and what it would take to resolve it.

---

## 1. EV Charging Station Management

**Manager Requirement:** EV chargers are tied to specific designated parking spots. Non-EVs should not occupy EV bays. The system must track charging statuses (Available, Charging, Faulted, Offline).

**Debt Taken:**
- **Designated spots are a logical split, not a physical one.** The prototype maintains two arrays (`slots` and `evSlots`) but has no concept of a physical bay, charger hardware ID, or OCPP endpoint.
- **No charger state machine.** `chargeStatus()` only prints the vehicle's `charge` attribute (a static integer). It does not model charger states such as Available, Preparing, Charging, Suspended, Finishing, Faulted, or Offline.
- **No enforcement of EV-only occupancy.** The `park()` method routes by an `ev` boolean flag passed from the GUI. A malicious or buggy caller could park a non-EV in an EV slot.
- **No OCPP integration.** There is no communication layer for external charger hardware.

**Impact:** High. EV charging is a core domain, and the current implementation is only a placeholder.

**Pay-down Path:**
1. Introduce a `ChargerAsset` entity with state machine transitions.
2. Link each `EVBay` to a `ChargerAsset` and a physical connector ID.
3. Add OCPP adapter interface and vendor-specific implementations.
4. Enforce vehicle-to-bay validation at the domain layer.

---

## 2. Local Offline Autonomy

**Manager Requirement:** Facilities must remain operational (barriers, occupancy, ticketing, EV charging) during internet outages and sync when connectivity returns.

**Debt Taken:**
- **No persistent local storage.** State is held only in Python lists and integers in memory. A process restart wipes all data.
- **No sync / reconciliation logic.** There is no outbox pattern, no event log replay, and no conflict resolution for transactions that occurred while offline.
- **No edge-to-cloud communication layer.** The prototype runs entirely in a single Python process. There is no Facility Edge Service, no REST/gRPC API, and no Kafka event broker.

**Impact:** High. Offline autonomy was described as a hard operational requirement.

**Pay-down Path:**
1. Add a local SQLite/PostgreSQL database to the edge node for ACID durability.
2. Implement an event outbox that queues domain events locally.
3. Build a sync service that replays events to the cloud after reconnection.
4. Add conflict resolution rules (e.g., reservations win over drive-ups).

---

## 3. Domain & Ubiquitous Language (Parking Sessions)

**Manager Requirement:** Track a vehicle's full stay as a "Parking Session" with entry time, exit time, status, customer/account references, and payment state.

**Debt Taken:**
- **No session entity.** The prototype returns a `slotid` as a primitive integer. There is no `ParkingSession` aggregate root with lifecycle states (Active, PaymentPending, Completed, Cancelled).
- **No temporal tracking.** Entry time and exit time are not recorded. Duration-based pricing cannot be calculated.
- **No customer or account linkage.** The prototype does not know about monthly subscribers, reservations, or saved payment methods.
- **No ticket / credential abstraction.** The `slotid` is a stand-in for a physical or digital ticket, but there is no `Ticket` entity with barcode, QR code, or LPR correlation.

**Impact:** Medium-High. Session tracking is foundational for billing, reporting, and customer experience.

**Pay-down Path:**
1. Create a `ParkingSession` aggregate root with entry/exit timestamps, status, and foreign keys to `CustomerAccount`.
2. Integrate with the Customer Identity Service for subscription validation.
3. Generate proper `Ticket` or `AccessCredential` value objects at entry.

---

## 4. Reservations & Capacity Management

**Manager Requirement:** Support advanced bookings with reserved capacity buffers. During degraded/offline mode, reservations must take priority over drive-up traffic.

**Debt Taken:**
- **No reservation entity or API.** The prototype has no concept of a reservation, booking window, or capacity buffer.
- **No priority rules.** All parking requests are treated as first-come-first-served drive-ups.
- **No degraded mode logic.** The system does not distinguish between Online, Offline, and Degraded operating modes.
- **No yield management.** There is no overbooking strategy, no waitlist, and no dynamic buffer adjustment.

**Impact:** Medium. Reservations are a supporting subdomain, but they are critical for high-utilization facilities.

**Pay-down Path:**
1. Introduce a `Reservation` aggregate with time windows and status transitions.
2. Add a capacity buffer to `FacilityInventory` that is reserved for confirmed reservations.
3. Implement priority rules in the entry-decision logic (reservations > subscribers > drive-ups).

---

## 5. Traceability, Auditability, and Event Streaming

**Manager Requirement:** Event streaming and audit trails for cross-facility reporting, transaction reconciliation, and analytics.

**Debt Taken:**
- **In-process event bus only.** The prototype uses a simple observer list (`event_observers`) inside `ParkingLot`. Events are delivered synchronously within the same thread.
- **No persistence or replay.** Published events are not durably logged. If the GUI is not listening, the event is lost.
- **No schema versioning.** Event classes are ad-hoc Python objects. There is no forward/backward compatibility strategy.
- **No cross-facility visibility.** Each `ParkingLot` instance is isolated. There is no central event store or analytics pipeline.

**Impact:** Medium. The scaffolding is correct (typed domain events), but the infrastructure is missing.

**Pay-down Path:**
1. Replace the in-process observer list with an asynchronous message broker (e.g., Kafka, RabbitMQ).
2. Add an event store (e.g., event-sourced PostgreSQL, Kafka log compaction) for durability and replay.
3. Define Avro/Protobuf schemas for all domain events with versioning rules.
4. Build a reporting service that consumes events for cross-facility dashboards.

---

## 6. Facility Variability and Vehicle Types

**Manager Requirement:** Different facilities have different business rules, access mechanisms (boom gates vs. LPR), and vehicle policies.

**Debt Taken:**
- **Single hardcoded facility in GUI.** The core domain architecture (`ParkingLot` class) is fully decoupled and supports scaling to multiple facilities concurrently. However, the `AppGUI` prototype is hardcoded to hold only a single `ParkingLot` reference at a time. Managing multiple lots concurrently (e.g., via a dashboard or dropdown) is not implemented in the UI.
- **No facility-specific rule overrides.** Pricing is pluggable via Strategy, but access mechanisms, operating hours, and vehicle-type policies are not configurable per facility.
- **No physical access control integration.** The GUI simulates entry/exit with buttons. There is no integration with boom gates, LPR cameras, or ticket dispensers.

**Impact:** Medium. The Strategy pattern and Factory pattern provide the right extension points, but the configuration layer is missing.

**Pay-down Path:**
1. Add a `Facility` entity with site-specific configuration (access mechanism, tariffs, operating rules).
2. Build hardware adapter interfaces for gates, LPR, and kiosks.
3. Move vehicle-type policies from the factory into facility-specific rule engines.

---

## 7. Billing, Pricing & Settlement

**Manager Requirement:** Support unified billing (parking + charging combined), idle fees, third-party revenue sharing, and split settlement scenarios.

**Debt Taken:**
- **Simplified pricing model.** The Strategy pattern supports flat rate, EV surcharge, and vehicle-type rates, but it does **not** model:
  - Time-based or duration-based pricing (no entry/exit timestamps).
  - Idle fees after charging completes.
  - Combined parking + charging invoices.
  - Tax treatment differences between parking and electricity.
- **No payment gateway integration.** Fees are calculated but never charged.
- **No settlement or revenue sharing.** There is no ledger for splitting revenue between EasyParkPlus, landlords, and third-party charger operators.

**Impact:** High. Billing is where the business makes money, and the current implementation is a toy model.

**Pay-down Path:**
1. Introduce time-tracking in `ParkingSession` and `ChargingSession` to enable duration-based fees.
2. Build a `BillingEngine` that composes line items (parking fee, charging fee, idle fee) into a `UnifiedInvoice`.
3. Integrate with Stripe or another payment gateway for transaction processing.
4. Add a `SettlementBatch` aggregate for revenue reconciliation and vendor payouts.

---

## 8. Security & Data Integrity

**Manager Requirement:** Prevent duplicate payments, ensure accurate occupancy near capacity, and validate monthly subscriber access.

**Debt Taken:**
- **No authentication or authorization.** Anyone with GUI access can park or remove any vehicle.
- **No duplicate payment protection.** The prototype does not process payments, so idempotency keys and payment deduplication are not implemented.
- **Race conditions possible.** The in-memory slot arrays are not thread-safe. Concurrent `park()` or `leave()` calls could corrupt occupancy counts.

**Impact:** High for production; acceptable for a prototype.

**Pay-down Path:**
1. Add JWT-based authentication and role-based access control (RBAC).
2. Use database transactions with optimistic locking for slot allocation.
3. Implement idempotency keys for all payment and settlement operations.

---

## Summary

| Area | Debt Level | Prototype Scaffolding | Missing for Production |
|------|------------|----------------------|------------------------|
| EV Charging | High | `evSlots`, `chargeStatus()` | Charger state machine, OCPP, bay enforcement |
| Offline Autonomy | High | In-memory local state | Persistent edge DB, sync, reconciliation |
| Parking Sessions | High | `slotid` primitive | `ParkingSession` aggregate, timestamps, customer linkage |
| Reservations | Medium | Capacity counters | Reservation entity, priority rules, buffers |
| Event Streaming | Medium | Typed `DomainEvent` classes | Async broker, event store, schema versioning |
| Facility Variability | Medium | Strategy + Factory patterns | Multi-facility config, hardware adapters |
| Billing & Settlement | High | `PricingStrategy` hierarchy | Duration pricing, unified invoice, payment gateway |
| Security | High | Basic input validation | Auth, RBAC, transactional slot locking |


