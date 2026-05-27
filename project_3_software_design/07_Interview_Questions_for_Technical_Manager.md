# Interview Questions for Michael (Technical Manager)

To effectively design the Domain-Driven Design (DDD) model and the proposed microservices architecture, we need to gather more context from Michael, the Technical Manager at EasyParkPlus. 

Here is a comprehensive list of questions organized by topic, along with Michael's answers: https://chatgpt.com/s/t_6a131e2084cc819198644256286f5546

## 1. Scaling to Multiple Facilities

**Q: Scale & Scope: How many parking facilities are we scaling to initially, and what is the expected growth rate over the next few years?**

**A:** Currently, EasyParkPlus operates 10 multi-story parking facilities across Boston, New York City, and Philadelphia. For the EV rollout, the initial scaling target is to equip all 10 sites with charging capabilities in phases over the first 18–24 months. From the business side, leadership is projecting roughly 15–20% growth in facility count over the next 3–5 years, primarily through additional urban garages and partnerships with commercial property operators.

**Q: Facility Independence: Do individual parking facilities need to remain operational if they lose internet connection to the central servers (i.e., do they need local offline autonomy)?**

**A:** Yes, each parking facility absolutely needs local offline autonomy. Internet outages are fairly common in garages, especially on underground levels. At a minimum, the site must continue handling:
* Vehicle entry/exit barriers
* Ticketing and payment processing
* EV charger session continuation
* Local occupancy tracking

Once connectivity returns, the site can sync transactions and operational records back to the central systems.

**Q: Variability: Do different facilities have different pricing models, business rules, or physical access mechanisms (e.g., some have boom gates, others have license plate recognition)?**

**A:** Yes, our facilities are not fully standardized today. Different sites have different operational setups depending on age, location, and ownership agreements. Examples include:
* Some garages use boom gates with ticket dispensers.
* Newer sites use only License Plate Recognition (LPR).
* Monthly parking rules differ by city and landlord contracts.
* EV charging tariffs may vary by facility and utility provider.

Therefore, operational rules are definitively site-specific in several areas.

**Q: Customer Base: Are user accounts and payment methods global across all EasyParkPlus facilities, or are they localized?**

**A:** The intention is for customer accounts and payment methods to be global across all EasyParkPlus facilities. A customer should be able to use the same account, subscription, and stored payment method in any of our garages. However, some legacy facilities still rely on older, local-only systems today, especially for monthly parking memberships. Consolidating those into a shared, company-wide customer platform is part of the modernization effort.

## 2. EV Charging Station Management (New Domain)

**Q: Physical Layout: How are the EV chargers mapped to parking spots? Are they only available in designated spots, or across the whole facility?**

**A:** EV chargers are tied to specific, designated parking spots, not spread across every space in the facility. Typically:
* One charger is assigned to one EV-designated parking bay.
* Some dual-port chargers can serve two adjacent bays.
* Premium areas may reserve charger spots for subscribers or valet use.
* Non-EV vehicles are not supposed to occupy those bays, though enforcement varies by site.

The charger and parking spot are operationally linked at the facility level.

**Q: Billing & Pricing: How does EV charging billing work? Is it billed by time (minutes), by energy consumed (kWh), or a flat fee?**

**A:** Today, the industry uses a mix of billing models, and we expect EasyParkPlus to support several depending on the facility and local regulations. The most common models are:
* Billing by energy consumed (kWh) — preferred for public charging.
* Billing by charging duration (minutes/hours).
* Flat session fees (used in some older setups).
* Combined or separate parking and charging fees.

Some cities and utilities have regulations affecting which pricing methods are legally allowed, so this can vary by location.

**Q: Consolidated Billing: Should the parking fee and the EV charging fee be combined into a single transaction for the customer, or handled as separate payments?**

**A:** From a customer experience perspective, we prefer a single, combined transaction whenever possible. Drivers generally expect one receipt covering both parking and EV charging. Operationally, though, there are cases where they may remain separate:
* Third-party charger operators.
* Different tax treatments for electricity vs. parking.
* Monthly parking subscribers paying only for charging usage.
* Failed or interrupted charging sessions needing adjustment.

While the business preference is unified billing, the system needs the flexibility for split settlement scenarios.

**Q: Idle Fees: How do we handle situations where a car has finished charging but continues to occupy the EV spot? Are there idle fees or notifications sent to the user?**

**A:** Yes, we plan to use both notifications and idle fees to manage charger availability, as EV spots are limited resources in our garages. Typical handling includes:
* Sending an app or SMS notification when charging completes.
* Allowing a short grace period (usually 10–20 minutes).
* Applying idle occupancy fees after the grace period.
* In premium locations, staff may also intervene or relocate vehicles if policy allows.

The exact idle fee rules can differ by facility and local market conditions.

**Q: Hardware Integration: Does the system need to communicate with external 3rd-party EV charger APIs (like OCPP), or are these proprietary EasyParkPlus stations?**

**A:** We definitely expect integration with external charger systems rather than exclusively using proprietary hardware, as we do not manufacture chargers ourselves. Most new deployments will use industry-standard protocols like the Open Charge Point Protocol (OCPP), since different facilities may use different charger vendors over time. Some older sites may also have vendor-specific APIs or cloud platforms that need separate integration. Vendor flexibility is important for procurement and maintenance operations.

**Q: Charger States: What are the operational states of a charger we need to track (e.g., Available, Preparing, Charging, Suspended, Faulted)?**

**A:** Operational status tracking is highly important for both customer visibility and maintenance teams. The main charger states we typically care about are:
* Available
* Occupied / Connected
* Preparing
* Charging
* Suspended / Paused
* Finishing
* Faulted / Out of Service
* Offline / Communication Lost

We also usually track whether the physical parking bay itself is occupied, separately from the charger state.

## 3. Domain & Ubiquitous Language

**Q: Actors: Who are the primary users of the system (e.g., Drivers, Facility Managers, Maintenance Technicians, Customer Support)?**

**A:** The system will serve several different operational groups across EasyParkPlus. The primary users are:
* Drivers / Customers
* Facility Managers for each garage
* Parking Attendants and Valet Staff
* Maintenance Technicians for parking and charger equipment
* Customer Support Agents
* Corporate Operations and Finance Teams

Each group needs different visibility and permissions based on their operational role.

**Q: Terminology: What are the exact business terms used for a vehicle entering and leaving? (e.g., is it called a "Parking Session", a "Ticket", a "Visit"?)**

**A:** Internally, we most commonly refer to a vehicle's full stay as a "Parking Session." That starts at entry and ends at exit. Other related terms we use are:
* "Ticket" — usually the physical or digital access credential.
* "Visit" — sometimes used in customer-facing reporting.
* "Monthly Parking Session" — for subscriber activity.
* "Charging Session" — used separately for EV energy usage.

Operationally, "Parking Session" is probably the clearest core business term.

**Q: Core vs. Generic Subdomains: Besides Parking Management and EV Charging, what other subdomains exist? (e.g., is Billing considered a core competitive advantage, or a generic subdomain we can outsource to Stripe?)**

**A:** Besides Parking Management and EV Charging, we also deal with several supporting operational areas. Key subdomains are:
* Customer Accounts & Memberships
* Billing and Payments
* Access Control & Gate Systems
* Reservations and Space Inventory
* Enforcement and Violations
* Maintenance & Asset Management
* Reporting, Finance, and Audits

From a business perspective, billing itself is not really our competitive advantage. We would likely rely on external payment providers for payment processing, while keeping our own pricing rules, validations, and operational records internally.

## 4. Microservices Architecture & Data

**Q: Consistency: Are there any operations that require strict transactional consistency, or is eventual consistency acceptable across microservices (e.g., between the Payment service and the Analytics service)?**

**A:** Some operations definitely require strict consistency from the business side, especially where money, access, or legal liability are involved. Examples needing strong consistency include:
* Processing successful payment before the exit gate opens.
* Preventing duplicate charging/payment records.
* Maintaining accurate occupancy counts when facilities are near capacity.
* Validating monthly subscriber access.

For reporting, analytics, utilization dashboards, and historical trends, eventual consistency is usually acceptable.

**Q: Technology Constraints: Are there any strict constraints regarding the database technologies or communication protocols (e.g., REST, gRPC, Kafka) we should assume for the new architecture?**

**A:** From the operations side, we don’t mandate specific database technologies, but we do care about reliability and vendor support. For communication, we generally expect:
* Real-time operations (gates, chargers): Low-latency APIs or streaming (often message-based).
* Integration with external systems (chargers, payment providers): REST-based APIs are most common.
* Event streaming: Useful for audit trails and cross-facility reporting.

We don’t have strict constraints like “must use one database or protocol,” but whatever is chosen needs to support high availability, offline recovery at the facility level, and strong auditability for transactions like parking sessions and payments.

**Q: Migration: Does the new architecture need to support data migration from the current prototype's data store?**

**A:** Yes, we’ll need to support data migration from the current prototype system. In practice, this includes:
* Active customer accounts and stored payment methods.
* Existing monthly parking contracts.
* Open or in-progress parking sessions (where applicable).
* Charger and facility configuration data.
* Historical transaction records for finance and audits.

We don’t expect a perfect one-time cutover. Some sites may migrate in phases, so the architecture should tolerate dual-running during the transition.

## 5. System Ownership & Source of Truth

**Q: Tariff & Pricing Management: Who owns the "source of truth" for pricing rules? Are tariffs managed centrally and pushed down to the facilities, or do facility managers configure pricing locally?**

**A:** Pricing ownership is mixed, depending on the type of rule:
* Core pricing strategy (base parking rates, EV charging tariffs, discounts) is centrally defined by corporate operations.
* These rules are then pushed down to each facility for execution.
* Facility managers can sometimes apply local overrides, but only within predefined bounds (e.g., event pricing, peak adjustments).
* Regulatory or landlord-driven pricing constraints may also force local variations in some sites.

So the "source of truth" is mostly central, but with controlled local flexibility where needed.

**Q: 3rd-Party Settlement: Since we integrate with 3rd-party charger operators, do we need a dedicated "Settlement/Clearing" subdomain to handle the revenue split between EasyParkPlus and the external vendors?**

**A:** Yes, we definitely need a dedicated Settlement/Clearing subdomain for third-party charger integrations. When we use external EV charging operators, the money flow isn’t simple:
* The customer pays a single session amount (often combined parking + charging).
* We need to split revenue between EasyParkPlus and the charger operator.
* Some sites also involve landlord revenue shares.

This requires:
* Tracking gross vs. net amounts per session.
* Applying contract-specific revenue share rules.
* Reconciling vendor invoices vs. actual usage data.
* Handling adjustments (idle fees, refunds, failed sessions).

Therefore, it should be a distinct operational domain separate from billing and payments.

**Q: Reservations during Outages: If a facility is offline, how do we handle new reservations made via the central cloud app? Are reservations temporarily disabled for that facility, or is there a conflict resolution strategy when the facility comes back online and spots were taken by drive-up customers?**

**A:** In practice, we don’t disable reservations just because a facility is offline — that would create customer frustration. Instead:
* Reservations continue to be accepted centrally.
* The facility uses a reserved capacity buffer (we never sell 100% of spots).
* If offline, the site runs in "degraded mode" and prioritizes honoring existing reservations at entry.
* Walk-in/drive-up customers are allowed only within the remaining live capacity.
* Upon reconnection, we reconcile occupancy using entry/exit logs and adjust availability.

Conflicts (which are rare but possible) are resolved with priority rules: reservations > subscriptions > drive-up traffic.
